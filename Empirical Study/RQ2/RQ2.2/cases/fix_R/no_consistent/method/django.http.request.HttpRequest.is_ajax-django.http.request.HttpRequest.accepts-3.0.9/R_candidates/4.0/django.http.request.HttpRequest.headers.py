    @cached_property
    def headers(self):
        return HttpHeaders(self.META)
