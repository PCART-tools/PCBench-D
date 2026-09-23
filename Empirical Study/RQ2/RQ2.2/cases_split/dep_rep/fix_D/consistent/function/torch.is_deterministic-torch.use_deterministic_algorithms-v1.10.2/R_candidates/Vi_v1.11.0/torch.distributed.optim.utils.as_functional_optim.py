def as_functional_optim(optim_cls: Type, *args, **kwargs):
    try:
        functional_cls = functional_optim_map[optim_cls]
    except KeyError:
        raise ValueError(f"Optimizer {optim_cls} does not have a functional counterpart!")

    return _create_functional_optim(functional_cls, *args, **kwargs)
