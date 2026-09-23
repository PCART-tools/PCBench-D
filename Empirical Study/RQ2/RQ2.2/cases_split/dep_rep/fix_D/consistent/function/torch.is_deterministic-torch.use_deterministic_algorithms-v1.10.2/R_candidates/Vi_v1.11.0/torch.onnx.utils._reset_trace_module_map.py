def _reset_trace_module_map():
    torch.jit._trace._trace_module_map = None
