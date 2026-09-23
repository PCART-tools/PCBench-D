def get_group_index(labels, shape, sort, xnull):
    """
    For the particular label_list, gets the offsets into the hypothetical list
    representing the totally ordered cartesian product of all possible label
    combinations, *as long as* this space fits within int64 bounds;
    otherwise, though group indices identify unique combinations of
    labels, they cannot be deconstructed.
    - If `sort`, rank of returned ids preserve lexical ranks of labels.
      i.e. returned id's can be used to do lexical sort on labels;
    - If `xnull` nulls (-1 labels) are passed through.

    Parameters
    ----------
    labels: sequence of arrays
        Integers identifying levels at each location
    shape: sequence of ints same length as labels
        Number of unique levels at each location
    sort: boolean
        If the ranks of returned ids should match lexical ranks of labels
    xnull: boolean
        If true nulls are eXcluded. i.e. -1 values in the labels are
        passed through
    Returns
    -------
    An array of type int64 where two elements are equal if their corresponding
    labels are equal at all location.
    """
    def loop(labels, shape):
        # how many levels can be done without overflow:
        pred = lambda i: not _int64_overflow_possible(shape[:i])
        nlev = next(filter(pred, range(len(shape), 0, -1)))

        # compute flat ids for the first `nlev` levels
        stride = np.prod(shape[1:nlev], dtype='i8')
        out = stride * labels[0].astype('i8', subok=False, copy=False)

        for i in range(1, nlev):
            stride //= shape[i]
            out += labels[i] * stride

        if xnull: # exclude nulls
            mask = labels[0] == -1
            for lab in labels[1:nlev]:
                mask |= lab == -1
            out[mask] = -1

        if nlev == len(shape):  # all levels done!
            return out

        # compress what has been done so far in order to avoid overflow
        # to retain lexical ranks, obs_ids should be sorted
        comp_ids, obs_ids = _compress_group_index(out, sort=sort)

        labels = [comp_ids] + labels[nlev:]
        shape = [len(obs_ids)] + shape[nlev:]

        return loop(labels, shape)

    def maybe_lift(lab, size):  # pormote nan values
        return (lab + 1, size + 1) if (lab == -1).any() else (lab, size)

    labels = map(com._ensure_int64, labels)
    if not xnull:
        labels, shape = map(list, zip(*map(maybe_lift, labels, shape)))

    return loop(list(labels), list(shape))
