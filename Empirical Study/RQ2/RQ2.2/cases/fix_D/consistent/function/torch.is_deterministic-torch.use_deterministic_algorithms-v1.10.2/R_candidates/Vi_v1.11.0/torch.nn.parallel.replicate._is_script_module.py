def _is_script_module(module):
    import torch.jit
    return isinstance(module, torch.jit.ScriptModule)
