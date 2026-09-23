def input_dtypes(event: _ProfilerEvent):
    assert isinstance(event.extra_fields, _ExtraFields_TorchOp)
    return tuple(getattr(i, "dtype", None) for i in event.extra_fields.inputs)
