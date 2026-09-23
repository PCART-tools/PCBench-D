    def is_cached(self, instance):
        return hasattr(instance, self.cache_name)
