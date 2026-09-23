def _conv_2d_shuffle_offsets(
    batch_size, kernel, dims, num_deformable_group, input_channels, output_channels
):
    o = []
    w0 = [[0 for x in range(kernel)] for y in range(kernel)]
    for y0 in range(0, kernel):
        for x0 in range(0, kernel):
            x = np.random.randint(0, kernel)
            y = np.random.randint(0, kernel)
            o.append(y - y0)
            o.append(x - x0)
            w0[y][x] += 1
    o = o * num_deformable_group
    e = []
    for v in o:
        e.append([[v] * int(dims[1])] * int(dims[0]))
    w0 = [[w0] * input_channels] * output_channels
    return (
        np.array([e] * batch_size).astype(np.float32),
        utils.NCHW2NHWC(np.array(w0).astype(np.float32)),
    )
