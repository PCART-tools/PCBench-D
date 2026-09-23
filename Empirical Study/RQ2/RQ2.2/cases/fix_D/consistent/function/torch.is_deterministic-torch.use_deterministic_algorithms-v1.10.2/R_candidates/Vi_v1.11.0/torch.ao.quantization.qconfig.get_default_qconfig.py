def get_default_qconfig(backend='fbgemm'):
    """
    Returns the default PTQ qconfig for the specified backend.

    Args:
      * `backend`: a string representing the target backend. Currently supports `fbgemm`
        and `qnnpack`.

    Return:
        qconfig
    """

    if backend == 'fbgemm':
        qconfig = QConfig(activation=HistogramObserver.with_args(reduce_range=True),
                          weight=default_per_channel_weight_observer)
    elif backend == 'qnnpack':
        qconfig = QConfig(activation=HistogramObserver.with_args(reduce_range=False),
                          weight=default_weight_observer)
    else:
        qconfig = default_qconfig
    return qconfig
