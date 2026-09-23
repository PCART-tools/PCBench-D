    @wraps(np.swapaxes)
    def swapaxes(self, axis1, axis2):
        return swapaxes(self, axis1, axis2)
