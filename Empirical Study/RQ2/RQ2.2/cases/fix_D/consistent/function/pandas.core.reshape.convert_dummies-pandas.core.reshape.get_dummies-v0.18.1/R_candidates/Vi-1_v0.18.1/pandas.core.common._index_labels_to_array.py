def _index_labels_to_array(labels):
    if isinstance(labels, (compat.string_types, tuple)):
        labels = [labels]

    if not isinstance(labels, (list, np.ndarray)):
        try:
            labels = list(labels)
        except TypeError:  # non-iterable
            labels = [labels]

    labels = _asarray_tuplesafe(labels)

    return labels
