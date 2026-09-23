def extract_weights(
    mod: nn.Module,
) -> tuple[tuple[Tensor, ...], tuple[str, ...], dict[str, list[str]]]:
    """
    This function removes all the Parameters from the model and
    return them as a tuple as well as their original attribute names.
    The weights must be re-loaded with `load_weights` before the model
    can be used again.
    Note that this function modifies the model in place and after this
    call, mod.parameters() will be empty.
    """
    return _extract_members(mod, mod.named_parameters, nn.Parameter)
