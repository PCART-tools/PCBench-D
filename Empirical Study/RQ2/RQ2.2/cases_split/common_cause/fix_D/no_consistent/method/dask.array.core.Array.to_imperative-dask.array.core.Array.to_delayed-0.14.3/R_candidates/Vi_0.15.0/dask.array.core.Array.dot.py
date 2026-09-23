    @wraps(np.dot)
    def dot(self, other):
        return tensordot(self, other,
                         axes=((self.ndim - 1,), (other.ndim - 2,)))
