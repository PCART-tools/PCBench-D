def lazy_tensor_decls(value_types: List[NamedCType], tensor_class: str) -> str:
    lazy_tensor_decls: List[str] = []
    for t in value_types:
        if isinstance(t.type, BaseCType):
            lazy_tensor_decls.append(
                f"{tensor_class} lazy_{t.name} = "
                f"GetLtcTensorOrCreateForWrappedNumber({t.name}, *device);")
        elif isinstance(t.type, OptionalCType):
            # TODO(alanwaketan): Maybe we want to apply GetLtcTensorOrCreateForWrappedNumber here, but hold it
            # until we encounter a real world example.
            lazy_tensor_decls.append(
                f"    {tensor_class} lazy_{t.name} = TryGetLtcTensor({t.name}.value_or(at::Tensor()));")
        else:
            raise AssertionError("TODO not sure if there are other valid types to handle here")
    return "\n    ".join(lazy_tensor_decls)
