def ref_gather(axis):
    def inner(data, ind):
        if ind.size == 0 or data.shape[axis] == 0:
            shape = list(data.shape)
            shape[0] = 0
            return [np.zeros(tuple(shape)).astype(np.float32)]
        # np.take() does axis lookup same as gather
        output = data.take(ind, axis).astype(np.float32)
        return [output]
    return inner
