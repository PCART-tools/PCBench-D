def add_loggers(
    name_a: str,
    model_a: torch.nn.Module,
    name_b: str,
    model_b: torch.nn.Module,
) -> Tuple[torch.nn.Module, torch.nn.Module]:
    """
    Enables intermediate activation logging on model_a and model_b.
    """
    _turn_on_loggers(name_a, model_a)
    _turn_on_loggers(name_b, model_b)
    return model_a, model_b
