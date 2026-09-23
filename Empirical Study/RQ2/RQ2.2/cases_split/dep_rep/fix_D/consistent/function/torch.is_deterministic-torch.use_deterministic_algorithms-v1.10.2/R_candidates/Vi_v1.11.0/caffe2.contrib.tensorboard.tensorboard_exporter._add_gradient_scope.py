def _add_gradient_scope(shapes, track_blob_names, ops):
    """
    For all operators or blobs with name containing "_grad", add a
    "GRADIENTS/" scope.

    Note: breaks graph execution since the blob -> gradient mapping is
    hardcoded.
    """
    def f(name):
        if '_grad' in name:
            return 'GRADIENTS/{}'.format(name)
        else:
            return name
    _rename_all(shapes, track_blob_names, ops, f)
