def divide_by_square_root(data, scale):
    output = np.copy(data)
    num_examples = len(scale)

    assert num_examples == data.shape[0]
    assert len(data.shape) == 2

    for i in range(0, num_examples):
        if scale[i] > 0:
            output[i] = np.multiply(data[i], 1 / math.sqrt(scale[i]))

    return (output, )
