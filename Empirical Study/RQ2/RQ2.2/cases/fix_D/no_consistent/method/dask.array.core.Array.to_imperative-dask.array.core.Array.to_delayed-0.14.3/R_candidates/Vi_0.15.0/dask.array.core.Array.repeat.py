    @wraps(np.repeat)
    def repeat(self, repeats, axis=None):
        return repeat(self, repeats, axis=axis)
