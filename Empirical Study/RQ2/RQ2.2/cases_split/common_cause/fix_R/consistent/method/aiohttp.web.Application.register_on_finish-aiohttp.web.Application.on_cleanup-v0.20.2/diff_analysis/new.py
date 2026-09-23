    def register_on_finish(self, func, *args, **kwargs):
        warnings.warn("Use .on_cleanup.append() instead", DeprecationWarning)
        self.on_cleanup.append(lambda app: func(app, *args, **kwargs))
