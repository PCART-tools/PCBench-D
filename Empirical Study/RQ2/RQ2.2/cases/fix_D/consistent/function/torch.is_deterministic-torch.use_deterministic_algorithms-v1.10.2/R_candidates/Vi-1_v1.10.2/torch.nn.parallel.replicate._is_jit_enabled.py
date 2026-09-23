def _is_jit_enabled():
    import torch.jit
    return torch.jit._state._enabled
