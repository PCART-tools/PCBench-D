def generate_type_hints(sig_group: PythonSignatureGroup) -> List[str]:
    type_hints: List[str] = []

    # Some deprecated ops that are on the blocklist are still included in pyi
    if sig_group.signature.name in blocklist and not sig_group.signature.deprecated:
        return type_hints

    # deprecated signatures have separate entries for their functional and out variants
    # (as opposed to the native ops, which fuse the two into a single signature).
    # generate the functional variant here, if an out variant exists.
    if sig_group.signature.deprecated and sig_group.outplace is not None:
        type_hint = sig_group.signature.signature_str_pyi(skip_outputs=True)
        type_hints.append(type_hint)

    # PythonSignatureGroups that have both a functional + out variant get a single signature, with an optional out argument
    # Generates the out variant if one exists. Otherwise, generate the functional variant
    type_hint = sig_group.signature.signature_str_pyi(
        skip_outputs=sig_group.outplace is None)
    type_hints.append(type_hint)

    # Some operators also additionally have a vararg variant of their signature
    type_hint_vararg = sig_group.signature.signature_str_pyi_vararg(
        skip_outputs=sig_group.outplace is None)
    if type_hint_vararg:
        type_hints.append(type_hint_vararg)

    return type_hints
