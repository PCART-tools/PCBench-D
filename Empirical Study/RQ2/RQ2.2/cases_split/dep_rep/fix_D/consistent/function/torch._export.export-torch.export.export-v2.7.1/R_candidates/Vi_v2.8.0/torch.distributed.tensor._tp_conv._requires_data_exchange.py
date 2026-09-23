def _requires_data_exchange(padding):
    # TODO: whether there requires data exchange is currently determined by padding
    return padding[1] != 0
