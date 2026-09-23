def _ns_and_class_name(full_qualname: str) -> tuple[str, str]:
    splits = full_qualname.split(".")
    assert len(splits) == 5, f"Could not split {full_qualname=}"
    _torch, _torch_ns, _classes, ns, class_name = splits
    return ns, class_name
