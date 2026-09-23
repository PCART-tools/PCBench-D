@torch.jit.script
def my_script_func(tensor):
    return torch.add(tensor, tensor)
