from rest_framework.permissions import BasePermission

from utils.http import POST


class IsOrganizationAdmin(BasePermission):
    # This permission is used for Organization based views

    message = 'User is not an admin of the organization'

    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.org_has_admin_user(user)


class IsAdminOrCreateOnly(BasePermission):
    message = 'User is not an admin of the organization'

    def has_object_permission(self, request, view, obj):
        if request.method == POST:
            return True

        user = request.user
        return obj.org_has_admin_user(user)


class IsOrganizationUser(BasePermission):
    message = 'User is not part of the organization'

    def has_object_permission(self, request, view, obj):
        if request.method == POST:
            return True

        user = request.user
        return obj.org_has_user(user)


class HasAdminPermission(BasePermission):
    # This permission is used for unified documents

    message = 'User does not have permission to view or create'

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'unified_document'):
            raise Exception('Object has no reference to unified document')

        unified_document = obj.unified_document
        permissions = unified_document.permissions
        return permissions.has_admin_user(request.user)


class HasEditingPermission(BasePermission):
    # This permission is used for unified documents

    message = 'User does not have permission to view or create'

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'unified_document'):
            raise Exception('Object has no reference to unified document')

        user = request.user
        unified_document = obj.unified_document
        permissions = unified_document.permissions
        is_admin = permissions.has_admin_user(user)
        is_editor = permissions.has_editor_user(user)
        return is_admin or is_editor


class HasAccessPermission(BasePermission):
    # This permission is used for unified documents

    message = 'User does not have permission to view or create'

    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'unified_document'):
            raise Exception('Object has no reference to unified document')

        unified_document = obj.unified_document
        permissions = unified_document.permissions
        return permissions.has_user(request.user)
