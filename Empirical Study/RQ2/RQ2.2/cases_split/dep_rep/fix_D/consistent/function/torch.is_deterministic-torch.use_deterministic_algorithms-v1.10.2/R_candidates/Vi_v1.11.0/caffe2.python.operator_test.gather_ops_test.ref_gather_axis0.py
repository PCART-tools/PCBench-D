def ref_gather_axis0():
    def inner(data, ind):
        if ind.size == 0 or data.shape[0] == 0:
            return [np.zeros((0, 10, 20)).astype(np.float32)]
        output = [data[i] for i in ind]
        return [output]
    return inner
