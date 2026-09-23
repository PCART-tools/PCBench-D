def ref_gather_match_outer(axis=1):
    def inner(data, ind):
        if ind.size == 0 or data.shape[axis] == 0:
            shape = list(data.shape)
            shape[0] = 0
            return [np.zeros(tuple(shape)).astype(np.float32)]
        input_shape = list(data.shape)
        output_shape = input_shape[:axis] + list(ind.shape[axis:]) + input_shape[axis + 1:]
        output = np.zeros(tuple(output_shape)).astype(np.float32)
        if axis == 1:
            for i in range(data.shape[0]):
                output[i] = data[i, ind[i], ]
        elif axis == 2:
            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    output[i, j] = data[i, j, ind[i, j], ]
        else:
            raise NotImplementedError
        return [output]
    return inner
