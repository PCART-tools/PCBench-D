def _recursive_to(inputs, target_device, use_side_stream_for_tensor_copies):
    r"""Recursively moves input to the target_device."""

    def to_map(obj):
        if isinstance(obj, (torch.Tensor, PackedSequence)):
            device = obj.data.device if isinstance(obj, PackedSequence) else obj.device
            if device == target_device:
                return (obj,)
            if not use_side_stream_for_tensor_copies:
                return (obj.to(target_device),)
            else:
                # If the custom module is not registered to torch, stream is not used for acceleration
                device_mod = getattr(torch, device.type, None)
                if device.type == "cpu" or device_mod is None:
                    return (obj.to(target_device),)

                from torch.nn.parallel._functions import _get_stream

                # Perform CPU -> target_device copies in a background stream. This code is
                # motivated from similar logic in torch/nn/parallel/_functions.py
                stream = _get_stream(target_device)
                with device_mod.stream(stream):
                    output = obj.to(target_device)
                # synchronize with the copy stream
                with device_mod.device(target_device.index):
                    current_stream = device_mod.current_stream()
                    # Sync the current stream with the copy stream
                    current_stream.wait_stream(stream)
                    # Ensure tensor memory is not reused until work on
                    # main stream is complete
                    if isinstance(obj, PackedSequence):
                        output.data.record_stream(current_stream)  # type: ignore[arg-type]
                    else:
                        assert isinstance(output, torch.Tensor)
                        output.record_stream(current_stream)  # type: ignore[arg-type]
                return (output,)

        from torch.nn.parallel.scatter_gather import _is_namedtuple

        if _is_namedtuple(obj):
            return [type(obj)(*args) for args in zip(*map(to_map, obj))]
        if isinstance(obj, tuple) and len(obj) > 0:
            return list(zip(*map(to_map, obj)))
        if isinstance(obj, list) and len(obj) > 0:
            return [list(i) for i in zip(*map(to_map, obj))]
        if isinstance(obj, dict) and len(obj) > 0:
            return [type(obj)(i) for i in zip(*map(to_map, obj.items()))]
        return [obj]

    # Avoid reference cycle
    try:
        res = to_map(inputs)
    finally:
        to_map = None  # type: ignore[assignment]
    return res
