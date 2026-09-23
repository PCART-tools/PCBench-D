def _RectifyInputOutput(blobs, net=None):
    """A helper function to rectify the input or output of the CreateOperator
    interface.
    """
    if isinstance(blobs, string_types) or isinstance(blobs, binary_type):
        # If blobs is a single string, prepend scope.CurrentNameScope()
        # and put it as a list.
        # TODO(jiayq): enforce using BlobReference instead of raw strings.
        return [ScopedBlobReference(blobs, net=net)]
    elif type(blobs) is BlobReference:
        # If blob is a BlobReference, simply put it as a list.
        return [blobs]
    elif type(blobs) in (list, tuple):
        # If blob is a list, we go through it and type check.
        rectified = []
        for blob in blobs:
            if isinstance(blob, string_types) or isinstance(blob, binary_type):
                rectified.append(ScopedBlobReference(blob, net=net))
            elif type(blob) is BlobReference:
                rectified.append(blob)
            else:
                raise TypeError(
                    "I/O blob #{} of unsupported type: {} of type {}"
                    .format(len(rectified), str(blob), type(blob)))
        return rectified
    else:
        raise TypeError(
            "Unknown input/output type: %s of type %s." %
            (str(blobs), type(blobs))
        )
