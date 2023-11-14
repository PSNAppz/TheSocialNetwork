from rest_framework import permissions

class IsNotGuestUserPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """
    message = 'guestuser: Permission denied'
    def has_permission(self, request, view):
        if request.user.uid == "guestuser":
            return False      
        return True