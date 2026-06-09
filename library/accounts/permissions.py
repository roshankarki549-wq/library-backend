from rest_framework.permissions import BasePermission


# Only users in the Admin group can access
class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        print("Current User:", request.user)
        print("Groups:", request.user.groups.all())

        # Check if logged-in user belongs to Admin group
        return request.user.groups.filter(
            name='Admin'
        ).exists()

from rest_framework.permissions import BasePermission

# Allow both Admin and Librarian users
class IsAdminOrLibrarian(BasePermission):

    def has_permission(self, request, view):

        # Check if user belongs to either group
        return request.user.groups.filter(
            name__in=['Admin', 'Librarian']
        ).exists()