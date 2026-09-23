def _init_script_module():
    import torch.jit
    return torch.jit.ScriptModule()
