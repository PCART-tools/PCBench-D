def _get_indices_dict(label_list, keys):
    shape = list(map(len, keys))

    group_index = get_group_index(label_list, shape, sort=True, xnull=True)
    ngroups = ((group_index.size and group_index.max()) + 1) \
              if _int64_overflow_possible(shape) \
              else np.prod(shape, dtype='i8')

    sorter = _get_group_index_sorter(group_index, ngroups)

    sorted_labels = [lab.take(sorter) for lab in label_list]
    group_index = group_index.take(sorter)

    return lib.indices_fast(sorter, group_index, keys, sorted_labels)
