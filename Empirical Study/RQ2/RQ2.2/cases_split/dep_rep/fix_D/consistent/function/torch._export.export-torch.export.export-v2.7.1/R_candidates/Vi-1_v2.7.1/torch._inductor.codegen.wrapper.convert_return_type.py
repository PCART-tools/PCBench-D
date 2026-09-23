def convert_return_type(ret: torch.Argument) -> str:
    # use x.real_type instead of x.type so that we get ScalarType instead of int
    python_type = repr(ret.real_type)  # type: ignore[attr-defined]
    python_to_cpp = {
        "Tensor": "at::Tensor",
        "List[Tensor]": "std::vector<at::Tensor>",
    }

    cpp_type = python_to_cpp.get(python_type, None)
    assert cpp_type is not None, f"NYI return type: {python_type}"
    # An output aliasing an input is returned by reference only when it's a
    # Tensor, not when it's a Tensor[]. For example, aten.split.Tensor's output
    # aliases the input tensor, but the op returns a vector by value.
    if python_type == "Tensor" and ret.alias_info is not None:
        cpp_type += "&"
    return cpp_type
