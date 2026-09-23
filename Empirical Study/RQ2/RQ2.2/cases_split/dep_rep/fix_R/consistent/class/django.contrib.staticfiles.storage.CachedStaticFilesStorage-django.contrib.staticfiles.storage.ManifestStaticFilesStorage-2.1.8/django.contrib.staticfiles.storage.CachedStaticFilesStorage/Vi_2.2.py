class CachedStaticFilesStorage(CachedFilesMixin, StaticFilesStorage):
    """
    A static file system storage backend which also saves
    hashed copies of the files it saves.
    """
    def __init__(self, *args, **kwargs):
        warnings.warn(
            'CachedStaticFilesStorage is deprecated in favor of '
            'ManifestStaticFilesStorage.',
            RemovedInDjango31Warning, stacklevel=2,
        )
        super().__init__(*args, **kwargs)
