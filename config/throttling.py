from rest_framework.throttling import SimpleRateThrottle


class FriendRequestRateThrottle(SimpleRateThrottle):
    scope = "friend_request_rate"

    def get_cache_key(self, request, view):
        print(request.user, "scope", self.scope)
        if request.user.is_authenticated:
            ident = request.user.pk
            return self.cache_format % {"scope": self.scope, "ident": ident}
