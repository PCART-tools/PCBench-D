def _is_script_method(module):
    import torch.jit
    return isinstance(module, torch._C.ScriptMethod)
