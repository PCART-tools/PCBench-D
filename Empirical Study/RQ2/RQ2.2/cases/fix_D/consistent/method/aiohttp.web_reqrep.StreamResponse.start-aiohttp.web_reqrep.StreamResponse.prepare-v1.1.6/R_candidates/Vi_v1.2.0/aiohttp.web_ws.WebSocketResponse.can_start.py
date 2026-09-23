    def can_start(self, request):
        warnings.warn('use .can_prepare(request) instead', DeprecationWarning)
        return self.can_prepare(request)
