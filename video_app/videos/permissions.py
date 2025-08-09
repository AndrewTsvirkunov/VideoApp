from rest_framework.permissions import BasePermission

class IsStaffOrOwnerOrPublished(BasePermission):
    """
    Object-level permission: staff sees all, published visible to all, owner sees own (включая unpublished).
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if obj.is_published:
            return True
        return obj.owner == request.user