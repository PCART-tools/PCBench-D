def concat(model, blobs_in, blob_out, **kwargs):
    """Depth Concat."""
    if kwargs.get('order') and kwargs.get('axis'):
        # The backend throws an error if both are given
        kwargs.pop('order')

    return model.net.Concat(
        blobs_in,
        [blob_out, "_" + blob_out + "_concat_dims"],
        **kwargs
    )[0]
