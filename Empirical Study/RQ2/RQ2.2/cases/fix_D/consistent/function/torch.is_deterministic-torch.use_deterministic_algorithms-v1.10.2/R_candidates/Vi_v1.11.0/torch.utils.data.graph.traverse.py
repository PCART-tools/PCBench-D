def traverse(datapipe, only_datapipe=False):
    if not isinstance(datapipe, IterDataPipe):
        raise RuntimeError("Expected `IterDataPipe`, but {} is found".format(type(datapipe)))

    items = list_connected_datapipes(datapipe, only_datapipe)
    d: Dict[IterDataPipe, Any] = {datapipe: {}}
    for item in items:
        d[datapipe].update(traverse(item, only_datapipe))
    return d
