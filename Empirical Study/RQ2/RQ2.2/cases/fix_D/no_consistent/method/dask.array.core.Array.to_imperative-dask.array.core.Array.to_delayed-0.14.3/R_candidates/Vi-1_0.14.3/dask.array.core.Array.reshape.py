    @wraps(np.reshape)
    def reshape(self, *shape):
        from .reshape import reshape
        if len(shape) == 1 and not isinstance(shape[0], Number):
            shape = shape[0]
        return reshape(self, shape)
