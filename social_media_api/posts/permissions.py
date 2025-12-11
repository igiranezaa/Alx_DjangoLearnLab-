from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    Only allow post/comment authors to edit or delete.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE METHODS = GET, HEAD, OPTIONS
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        return obj.author == request.user
