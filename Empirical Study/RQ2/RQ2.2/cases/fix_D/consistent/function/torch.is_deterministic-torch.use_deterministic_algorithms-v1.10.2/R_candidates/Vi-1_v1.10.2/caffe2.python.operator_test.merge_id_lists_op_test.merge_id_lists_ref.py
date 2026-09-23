def merge_id_lists_ref(*args):
    n = len(args)
    assert n > 0
    assert n % 2 == 0
    batch_size = len(args[0])
    num_inputs = int(n / 2)
    lengths = np.array([np.insert(args[2 * i], 0, 0)
                        for i in range(num_inputs)])
    values = [args[2 * i + 1] for i in range(num_inputs)]
    offsets = [np.cumsum(lengths[j]) for j in range(num_inputs)]

    def merge_arrays(vs, offs, j):
        concat = np.concatenate([vs[i][offs[i][j]:offs[i][j + 1]]
                                for i in range(num_inputs)])
        return np.sort(np.unique(concat))

    merged = [merge_arrays(values, offsets, j) for j in range(batch_size)]
    merged_lengths = np.array([len(x) for x in merged])
    merged_values = np.concatenate(merged)
    return merged_lengths, merged_values
