def EnsureNonBlockingDataPipe(validated_datapipe):
    if not isinstance(validated_datapipe, IterDataPipe):
        raise Exception('Not Iterable DataPipe ' +
                        str(validated_datapipe.__class__))
    if isinstance(validated_datapipe, NonBlocking):
        return validated_datapipe
    if not hasattr(validated_datapipe, '_as_iterator'):
        validated_datapipe._as_iterator = None  # type: ignore[attr-defined]
    if not hasattr(validated_datapipe, 'nonblocking_next'):
        def nonblocking_next(self):
            if self._as_iterator is None:
                self._as_iterator = iter(self)
            return next(self._as_iterator)
        validated_datapipe.nonblocking_next = types.MethodType(  # type: ignore[attr-defined]
            nonblocking_next, validated_datapipe)
    if not hasattr(validated_datapipe, 'reset_iterator'):
        def reset_iterator(self):
            self._as_iterator = None
        validated_datapipe.reset_iterator = types.MethodType(  # type: ignore[attr-defined]
            reset_iterator, validated_datapipe)
    return validated_datapipe
