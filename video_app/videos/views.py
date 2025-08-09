from django.db import transaction, IntegrityError
from django.db.models import Q, F, Sum, OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from .models import Video, Like
from .serializers import VideoSerializer
from .permissions import IsStaffOrOwnerOrPublished

from users.models import AppUser


# GET /v1/videos/{id}/
class VideoRetrieveView(generics.RetrieveAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Video.objects.select_related('owner').prefetch_related('files')
        if user.is_staff:
            return qs
        if user.is_authenticated:
            return qs.filter(Q(is_published=True) | Q(owner=user))
        return qs.filter(is_published=True)


# GET /v1/videos/  (paginate)
class VideoListView(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Video.objects.select_related("owner").prefetch_related("files")
        if user.is_staff:
            return qs
        if user.is_authenticated:
            return qs.filter(Q(is_published=True) | Q(owner=user))
        return qs.filter(is_published=True)


# GET /v1/videos/ids/   (admin only, no pagination)
class VideoIDsView(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        ids = list(Video.objects.filter(is_published=True).values_list('id', flat=True))
        return Response(ids)


# POST/DELETE /v1/videos/{video_id}/likes/
class LikeToggleView(views.APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, video_id):
        # likes allowed только для опубликованных видео
        video = get_object_or_404(Video, id=video_id, is_published=True)

        try:
            like, created = Like.objects.get_or_create(video=video, user=request.user)
        except IntegrityError:
            # конкурентное создание — считаем, что лайк уже существует
            created = False

        if created:
            # атомарный + F() — безопасно при гонках
            Video.objects.filter(pk=video.pk).update(total_likes=F('total_likes') + 1)
            return Response({'detail': 'liked'}, status=status.HTTP_201_CREATED)

        return Response({'detail': 'already_liked'}, status=status.HTTP_200_OK)

    @transaction.atomic
    def delete(self, request, video_id):
        video = get_object_or_404(Video, id=video_id, is_published=True)
        deleted, _ = Like.objects.filter(video=video, user=request.user).delete()
        if deleted:
            Video.objects.filter(pk=video.pk).update(total_likes=F("total_likes") - 1)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "not_found"}, status=status.HTTP_404_NOT_FOUND)


# /v1/videos/statistics-subquery/  (admins only)
class StatisticsSubqueryView(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        video_sum = (
            Video.objects.filter(is_published=True, owner=OuterRef("pk"))
            .values("owner")
            .annotate(likes_sum=Sum("total_likes"))
            .values("likes_sum")
        )

        qs = (
            AppUser.objects.annotate(
                likes_sum=Coalesce(Subquery(video_sum, output_field=IntegerField()), 0)
            )
            .values("username", "likes_sum")
            .order_by("-likes_sum")
        )
        return Response(list(qs))


# /v1/videos/statistics-group-by/  (admins only)
class StatisticsGroupByView(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = (
            AppUser.objects.filter(videos__is_published=True)
            .annotate(likes_sum=Sum("videos__total_likes"))
            .values("username", "likes_sum")
            .order_by("-likes_sum")
        )
        return Response(list(qs))


