def is_reuse_input_qconfig(qconfig: Optional[QConfig]):
    return qconfig is not None and \
        isinstance(qconfig.activation(), ReuseInputObserver) and \
        isinstance(qconfig.weight(), NoopObserver)
