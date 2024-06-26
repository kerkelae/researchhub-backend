from rest_framework.permissions import BasePermission

from utils.http import GET


class CanSetAsAcceptedAnswer(BasePermission):
    message = "User does not have permission to set answer"

    def has_object_permission(self, request, view, obj):
        user = request.user
        parent = obj.parent

        if parent:
            parent_creator = parent.created_by
            if parent_creator == user:
                return True

        # If the comment is a top level comment
        if not parent:
            document_creator = obj.thread.content_object.created_by
            if document_creator == user:
                return True

        return False


class ThreadViewingPermissions(BasePermission):
    message = "User does not have permission to view thread"

    def has_permission(self, request, view):
        user = request.user
        organization = getattr(request, "organization", None)
        if request.method == GET:
            organization_id = request.query_params.get("organization_id", None)

            if organization_id and not user.is_anonymous:
                if organization:
                    return organization.org_has_user(user)
            elif not organization_id:
                return True
            return False
        return True


class IsThreadCreator(BasePermission):
    message = "User is not creator of thread"

    def has_object_permission(self, request, view, obj):
        user = request.user
        thread = obj.thread
        return thread.created_by == user
