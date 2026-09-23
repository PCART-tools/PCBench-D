def _get_torch_cpp_wrapper_definition() -> list[str]:
    return ["TORCH_INDUCTOR_CPP_WRAPPER", "STANDALONE_TORCH_HEADER"]
