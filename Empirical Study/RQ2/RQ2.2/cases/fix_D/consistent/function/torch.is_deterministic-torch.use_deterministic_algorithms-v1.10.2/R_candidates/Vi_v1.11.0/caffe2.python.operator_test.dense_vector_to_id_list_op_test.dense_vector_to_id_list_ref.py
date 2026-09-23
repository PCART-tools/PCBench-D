def dense_vector_to_id_list_ref(*arg):
    arg = arg[0]
    batch_size = len(arg)
    assert batch_size > 0
    out_length = []
    out_values = []
    for row in arg:
        length = 0
        for idx, entry in enumerate(row):
            if entry != 0:
                out_values += [idx]
                length += 1
        out_length += [length]
    return (out_length, out_values)
