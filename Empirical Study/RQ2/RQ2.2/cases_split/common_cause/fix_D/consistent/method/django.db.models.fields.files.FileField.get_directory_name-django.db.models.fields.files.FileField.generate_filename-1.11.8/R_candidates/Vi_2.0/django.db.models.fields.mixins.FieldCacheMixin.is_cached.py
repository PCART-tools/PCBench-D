    def is_cached(self, instance):
        return self.get_cache_name() in instance._state.fields_cache
