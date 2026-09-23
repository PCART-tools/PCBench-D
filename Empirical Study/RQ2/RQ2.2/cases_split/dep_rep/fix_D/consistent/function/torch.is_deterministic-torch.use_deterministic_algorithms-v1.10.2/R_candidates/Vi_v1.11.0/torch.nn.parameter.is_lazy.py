def is_lazy(param):
    return isinstance(param, UninitializedTensorMixin)
