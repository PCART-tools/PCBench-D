def _get_dup_signature_tuples(fn: Callable) -> List[Tuple[str, str]]:
    """
    Helper that inspects the arg signature of `fn` and returns a list of tuples, where
    each tuple is a pair of duplicated names which is used for arg_replacement_tuples.
    """
    sig_tuples: List[Tuple[str, str]] = []
    for param in inspect.signature(inspect.unwrap(fn)).parameters:
        sig_tuples.append((param, param))
    return sig_tuples
