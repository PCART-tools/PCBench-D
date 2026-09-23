def EnsureNonBlockingMapDataPipe(validated_datapipe):
    if not isinstance(validated_datapipe, MapDataPipe):
        raise Exception(f'Not Map DataPipe - got {validated_datapipe.__class__}')
    if isinstance(validated_datapipe, NonBlockingMap):
        return validated_datapipe
    if not hasattr(validated_datapipe, 'nonblocking_len'):
        def nonblocking_len(self):
            return self.__len__()
        validated_datapipe.nonblocking_len = types.MethodType(  # type: ignore[attr-defined]
            nonblocking_len, validated_datapipe)
    if not hasattr(validated_datapipe, 'nonblocking_getitem'):
        def nonblocking_getitem(self, index):
            return self.__getitem__(index)
        validated_datapipe.nonblocking_getitem = types.MethodType(  # type: ignore[attr-defined]
            nonblocking_getitem, validated_datapipe)
    return validated_datapipe
