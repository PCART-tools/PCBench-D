    @cached_property
    def compiler_module(self):
        if self.connection.features.has_fetch_offset_support:
            return super().compiler_module
        return 'django.db.backends.oracle.compiler'
