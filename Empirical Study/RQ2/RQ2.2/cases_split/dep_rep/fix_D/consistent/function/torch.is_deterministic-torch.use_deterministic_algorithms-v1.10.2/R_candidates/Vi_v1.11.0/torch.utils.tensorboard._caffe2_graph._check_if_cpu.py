def _check_if_cpu(blob):
    '''
    Check if the blob's name starts with '_gpu'.

    Args:
        blob: The blob to inspect

    Returns:
        Boolean representing whether this blob is associated with a gpu
    '''
    return not blob.startswith('_gpu')
