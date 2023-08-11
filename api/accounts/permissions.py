from rest_framework import permissions


class TablesPermission(permissions.BasePermission):
    message = "You don't have permissions for tables actions"

    def has_permission(self, request, view):
        user = request.user
        if view.action == "list":
            return user.is_authenticated
        elif view.action == "create":
            return all([user.is_authenticated, user.has_perm("accounts.add_table")])
        elif view.action == "update":
            return all([user.is_authenticated, user.has_perm("accounts.remove_table")])
        elif view.action == "retrieve":
            return all(
                [user.is_authenticated, user.has_perm("accounts.retrieve_table")]
            )


class PlayerManagePermission(permissions.BasePermission):
    message = "You can't manage users"

    def has_permission(self, request, view):
        manage_func = ["create", "update", "delete"]
        user = request.user
        if view.action == "list":
            return user.is_authenticated
        elif view.action in manage_func:
            return all([user.is_authenticated, user.has_perm("accounts.manage_player")])
