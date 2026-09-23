def run_once(model: Callable, inp: InputsType, task: str, v: VType) -> None:
    func = getattr(functional, task)

    if v is not None:
        res = func(model, inp, v=v, strict=True)
    else:
        res = func(model, inp, strict=True)
