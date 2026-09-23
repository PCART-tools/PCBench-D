def _check_if_forward(blob):
    '''
    Blobs with names containing '_m' or 'grad' are part of the backward pass.
        This function references facebookresearch/Detectron/detectron/utils/net.py.

    Args:
        blob: The blob to inspect

    Returns:
        Boolean representing whether this blob is part of the forward pass
    '''
    #
    return (blob.find('__m') < 0 or blob.find('grad') < 0)
