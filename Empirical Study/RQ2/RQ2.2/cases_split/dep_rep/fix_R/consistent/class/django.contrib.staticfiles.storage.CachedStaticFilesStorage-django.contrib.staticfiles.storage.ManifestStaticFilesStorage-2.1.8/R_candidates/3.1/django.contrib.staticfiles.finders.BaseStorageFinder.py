class BaseStorageFinder(BaseFinder):
    """
    A base static files finder to be used to extended
    with an own storage class.
    """
    storage = None

    def __init__(self, storage=None, *args, **kwargs):
        if storage is not None:
            self.storage = storage
        if self.storage is None:
            raise ImproperlyConfigured("The staticfiles storage finder %r "
                                       "doesn't have a storage class "
                                       "assigned." % self.__class__)
        # Make sure we have a storage instance here.
        if not isinstance(self.storage, (Storage, LazyObject)):
            self.storage = self.storage()
        super().__init__(*args, **kwargs)

    def find(self, path, all=False):
        """
        Look for files in the default file storage, if it's local.
        """
        try:
            self.storage.path('')
        except NotImplementedError:
            pass
        else:
            if self.storage.location not in searched_locations:
                searched_locations.append(self.storage.location)
            if self.storage.exists(path):
                match = self.storage.path(path)
                if all:
                    match = [match]
                return match
        return []

    def list(self, ignore_patterns):
        """
        List all files of the storage.
        """
        for path in utils.get_files(self.storage, ignore_patterns):
            yield path, self.storage
