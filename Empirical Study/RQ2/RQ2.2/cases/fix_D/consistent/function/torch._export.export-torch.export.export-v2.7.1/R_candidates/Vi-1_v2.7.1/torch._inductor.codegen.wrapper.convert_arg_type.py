def convert_arg_type(arg: torch.Argument) -> str:
    from .cpp import CONTAINER_PYTHON_TO_CPP, PYTHON_TO_CPP

    # use x.real_type instead of x.type so that we get ScalarType instead of int
    python_type = repr(arg.real_type)  # type: ignore[attr-defined]

    if python_type == "Tensor":
        # Conversions rules follow https://github.com/pytorch/pytorch/tree/main/aten/src/ATen/native#func
        if arg.alias_info is not None and arg.alias_info.is_write:
            return f"at::{python_type}&"
        else:
            return f"at::{python_type} const&"

    if python_type in PYTHON_TO_CPP:
        cpp_type = PYTHON_TO_CPP[python_type]
        return cpp_type

    # Convert args of container types e.g. Optional[*]
    for py_container, cpp_container in CONTAINER_PYTHON_TO_CPP.items():
        container_match = re.findall(py_container + r"\[([a-zA-Z_]+)]", python_type)
        if len(container_match) == 1:
            contained_type = container_match[0]
            assert contained_type in PYTHON_TO_CPP, (
                f"unsupported {py_container} type in convert_arg_type: {contained_type}"
            )
            cpp_contained_type = PYTHON_TO_CPP[contained_type]
            return f"{cpp_container}<{cpp_contained_type}>"

    raise AssertionError(f"unsupport python_type: {python_type}")
