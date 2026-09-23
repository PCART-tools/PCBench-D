@torch.jit.script
def list_create() -> List[int]:
    global_list = [1, 2, 3]
    return global_list
