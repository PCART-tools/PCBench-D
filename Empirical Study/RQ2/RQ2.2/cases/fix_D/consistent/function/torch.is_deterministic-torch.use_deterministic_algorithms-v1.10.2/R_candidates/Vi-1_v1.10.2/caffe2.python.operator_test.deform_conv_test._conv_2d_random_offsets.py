def _conv_2d_random_offsets(batch_size, kernel, dims, num_deformable_group):
    o = []
    for y0 in range(0, kernel):
        for x0 in range(0, kernel):
            # stay away from integer offsets which correspond to "ridges" on the
            # interpolated surface resulting in less precise estimates
            x = np.random.randint(0, kernel) + np.random.uniform(0.05, 0.95)
            y = np.random.randint(0, kernel) + np.random.uniform(0.05, 0.95)
            o.append(y - y0)
            o.append(x - x0)
    o = o * num_deformable_group
    e = []
    for v in o:
        e.append([[v] * dims[1]] * dims[0])
    return np.array([e] * batch_size).astype(np.float32)
