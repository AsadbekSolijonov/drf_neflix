from rest_framework.throttling import UserRateThrottle, SimpleRateThrottle


# class BurstRateThrottle(UserRateThrottle):
    # scope = 'burst'


# class SustainedRateThrottle(UserRateThrottle):
    # scope = 'sustained'


# class PermiumRateThrottle(SimpleRateThrottle):
    # scope = 'premium'

    # def get_cache_key(self, request, view):
    #     if request.user.is_authenticated and request.user.status == 'premium':
    #         ident = request.user.pk  # ID
    #     else:
    #         ident = self.get_ident(request)  # IP address
    #     return self.cache_format % {'scope': self.scope, 'ident': ident}

