    @wraps(store)
    def store(self, target, **kwargs):
        return store([self], [target], **kwargs)
