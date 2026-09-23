def _get_onnx_devices(
    values: tuple[
        Union[
            torch.Tensor, torch.SymInt, int, torch.SymFloat, float, torch.SymBool, bool
        ],
        ...,
    ],
) -> tuple["ORTC.OrtDevice", ...]:
    from onnxruntime.capi import _pybind_state as ORTC

    def _device_id_or_zero(device_id: int) -> int:
        return device_id or 0

    def _map_tensor_or_sym_to_device(
        value: Union[
            torch.Tensor, torch.SymInt, int, torch.SymFloat, float, torch.SymBool, bool
        ],
    ) -> int:
        if isinstance(value, torch.Tensor):
            return ORTC.OrtDevice(
                _get_ort_device_type(value.device.type),
                ORTC.OrtDevice.default_memory(),
                _device_id_or_zero(value.device.index),
            )
        elif isinstance(
            value, (torch.SymInt, int, torch.SymFloat, float, torch.SymBool, bool)
        ):
            return ORTC.OrtDevice(
                _get_ort_device_type("cpu"), ORTC.OrtDevice.default_memory(), 0
            )
        else:
            raise ValueError("Unsupported value type: " + str(type(value)))

    if len(values) > 0:
        ort_devices = tuple(_map_tensor_or_sym_to_device(value) for value in values)
        return ort_devices
    else:
        return (_map_tensor_or_sym_to_device(1),)
