class DefaultStorageFinder(BaseStorageFinder):
    """
    A static files finder that uses the default storage backend.
    """
    storage = default_storage

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_location = getattr(self.storage, 'base_location', empty)
        if not base_location:
            raise ImproperlyConfigured("The storage backend of the "
                                       "staticfiles finder %r doesn't have "
                                       "a valid location." % self.__class__)
