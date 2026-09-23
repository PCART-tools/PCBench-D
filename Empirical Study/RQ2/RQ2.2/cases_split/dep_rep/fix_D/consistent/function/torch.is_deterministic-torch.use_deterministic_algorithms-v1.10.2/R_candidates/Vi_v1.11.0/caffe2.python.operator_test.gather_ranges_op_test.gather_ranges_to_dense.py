def gather_ranges_to_dense(data, ranges, lengths):
    outputs = []
    assert len(ranges)
    batch_size = len(ranges)
    assert len(ranges[0])
    num_ranges = len(ranges[0])
    assert ranges.shape[2] == 2
    for i in range(num_ranges):
        out = []
        for j in range(batch_size):
            start, length = ranges[j][i]
            if not length:
                out.append([0] * lengths[i])
            else:
                assert length == lengths[i]
                out.append(data[start : start + length])
        outputs.append(np.array(out))
    return outputs
