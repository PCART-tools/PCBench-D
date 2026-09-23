def ScopedBlobReference(name, *args, **kwargs):
    """Returns a blob reference with scope prefixed."""
    return BlobReference(ScopedName(name), *args, **kwargs)
