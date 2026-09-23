def unsupported_output_tensor(t: torch.Tensor, parent=None, node=None):
    "Do not support writing tensor but can read from it"
    if unsupported_input_tensor(t, parent):
        return True
    return t.is_cpu and config.disable_cpp_codegen
