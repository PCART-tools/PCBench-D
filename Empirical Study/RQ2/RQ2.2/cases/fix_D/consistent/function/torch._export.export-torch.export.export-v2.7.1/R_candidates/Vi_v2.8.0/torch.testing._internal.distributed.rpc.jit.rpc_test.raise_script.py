@torch.jit.script
def raise_script():
    raise RuntimeError("Expected error")
