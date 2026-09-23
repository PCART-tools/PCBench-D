    @wraps(chunk.nancumsum)
    def nancumsum(x, axis, dtype=None):
        return cumreduction(chunk.nancumsum, operator.add, 0, x, axis, dtype)
