def spec_to_bytes(spec: "dtensor_spec.DTensorSpec") -> int:
    assert spec.tensor_meta is not None, "spec should have tensor meta defined!"
    return spec.tensor_meta.dtype.itemsize * math.prod(spec.shape)
