def make_nancomp(op):
    def f(x, y):
        xmask = isnull(x)
        ymask = isnull(y)
        mask = xmask | ymask

        result = op(x, y)

        if mask.any():
            if is_bool_dtype(result):
                result = result.astype('O')
            np.putmask(result, mask, np.nan)

        return result
    return f
