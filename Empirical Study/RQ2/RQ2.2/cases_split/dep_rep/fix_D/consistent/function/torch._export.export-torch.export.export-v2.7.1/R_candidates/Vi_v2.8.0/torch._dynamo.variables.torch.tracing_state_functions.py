@functools.cache
def tracing_state_functions() -> dict[Callable[[], Any], Optional[bool]]:
    # Defined as a function to avoid circular import like torch.onnx
    return {
        torch.jit.is_scripting: False,
        torch.jit.is_tracing: False,
        torch._C._get_tracing_state: None,
        torch.fx._symbolic_trace.is_fx_tracing: False,
        torch.onnx.is_in_onnx_export: False,
        torch._dynamo.external_utils.is_compiling: True,
        torch._utils.is_compiling: True,
        torch.compiler.is_compiling: True,
        torch.compiler.is_dynamo_compiling: True,
        torch.compiler.is_exporting: True,
        torch.nn.modules.activation._is_make_fx_tracing: False,
    }
