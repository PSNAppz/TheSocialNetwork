from rest_framework.throttling import SimpleRateThrottle


class FriendRequestRateThrottle(SimpleRateThrottle):
    scope = "friend_request"

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
            return self.cache_format % {"scope": self.scope, "ident": ident}
