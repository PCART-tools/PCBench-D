def traverse(datapipe):
    items = list_connected_datapipes(datapipe)
    d: Dict[Any, Any] = {datapipe: {}}
    for item in items:
        d[datapipe].update(traverse(item))
    return d
