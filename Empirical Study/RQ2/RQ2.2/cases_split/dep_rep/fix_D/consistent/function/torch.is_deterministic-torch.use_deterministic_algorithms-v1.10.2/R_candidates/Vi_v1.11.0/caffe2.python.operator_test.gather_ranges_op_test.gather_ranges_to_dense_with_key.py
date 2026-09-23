def gather_ranges_to_dense_with_key(data, ranges, key, lengths):
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
                key_data_list = zip(
                    key[start : start + length], data[start : start + length]
                )
                sorted_key_data_list = sorted(key_data_list, key=lambda x: x[0])
                sorted_data = [d for (k, d) in sorted_key_data_list]
                out.append(sorted_data)
        outputs.append(np.array(out))
    return outputs
