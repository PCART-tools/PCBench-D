def _build_agg_args(spec):
    """
    Create transformation functions for a normalized aggregate spec.

    Parameters
    ----------
    spec: a list of (result-column, aggregation-function, input-column) triples.
        To work with all arugment forms understood by pandas use
        ``_normalize_spec`` to normalize the argment before passing it on to
        ``_build_agg_args``.

    Returns
    -------
    chunk_funcs: a list of (intermediate-column, function, keyword) triples
        that are applied on grouped chunks of the initial dataframe.

    agg_funcs: a list of (intermediate-column, functions, keword) triples that
        are applied on the grouped concatination of the preprocessed chunks.

    finalizers: a list of (result-column, function, keyword) triples that are
        applied after the ``agg_funcs``. They are used to create final results
        from intermediate representations.
    """
    known_np_funcs = {np.min: 'min', np.max: 'max'}

    chunks = {}
    aggs = {}
    finalizers = []

    for (result_column, func, input_column) in spec:
        func = funcname(known_np_funcs.get(func, func))
        impls = _build_agg_args_single(result_column, func, input_column)

        # overwrite existing result-columns, generate intermedates only once
        chunks.update((spec[0], spec) for spec in impls['chunk_funcs'])
        aggs.update((spec[0], spec) for spec in impls['aggregate_funcs'])

        finalizers.append(impls['finalizer'])

    chunks = sorted(chunks.values())
    aggs = sorted(aggs.values())

    return chunks, aggs, finalizers
