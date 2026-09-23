def get_v_for(model: Callable, inp: InputsType, task: str) -> VType:
    v: VType

    if task in ["vjp"]:
        out = model(*inp)
        v = torch.rand_like(out)
    elif task in ["jvp", "hvp", "vhp"]:
        if isinstance(inp, tuple):
            v = tuple(torch.rand_like(i) for i in inp)
        else:
            v = torch.rand_like(inp)
    else:
        v = None

    return v
