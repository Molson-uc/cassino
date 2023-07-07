from rest_framework import permissions


class TablesPermission(permissions.BasePermission):
    message = "Adding customers not allowed."

    def has_permission(self, request, view):
        user = request.user
        if view.action == "list":
            return user.is_authenticated()
        elif view.action == "create":
            return all(user.is_authenticated(), user.has_perm("accounts.add_table"))
        elif view.action == "update":
            return all(user.is_authenticated(), user.has_perm("accounts.remove_table"))
