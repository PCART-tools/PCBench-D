    @wraps(chunk.nancumprod)
    def nancumprod(x, axis, dtype=None, out=None):
        return cumreduction(chunk.nancumprod, operator.mul, 1, x, axis, dtype,
                            out=out)
