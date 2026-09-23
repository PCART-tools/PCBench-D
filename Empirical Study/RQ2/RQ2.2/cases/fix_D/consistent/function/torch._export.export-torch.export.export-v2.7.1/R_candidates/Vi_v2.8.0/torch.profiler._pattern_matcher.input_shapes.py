def input_shapes(event: _ProfilerEvent):
    assert isinstance(event.extra_fields, _ExtraFields_TorchOp)
    return tuple(tuple(getattr(i, "sizes", ())) for i in event.extra_fields.inputs)
