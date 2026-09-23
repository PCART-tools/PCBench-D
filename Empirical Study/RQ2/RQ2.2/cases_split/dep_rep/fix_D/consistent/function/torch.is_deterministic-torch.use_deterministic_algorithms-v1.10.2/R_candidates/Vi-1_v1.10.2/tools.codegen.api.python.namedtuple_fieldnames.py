def namedtuple_fieldnames(returns: Tuple[Return, ...]) -> List[str]:
    if len(returns) <= 1 or all(map(lambda r: r.name is None, returns)):
        return []
    else:
        if any(map(lambda r: r.name is None, returns)):
            # When building on Windows, `PyStructSequence_UnnamedField` could not be
            # resolved by the linker for some reason, which cause error in building:
            #
            # python_nn_functions.cpp.obj : error LNK2001: unresolved external symbol
            # PyStructSequence_UnnamedField
            #
            # Thus, at this point in time, we do not support unnamed
            # fields in namedtuple; you must either name all fields,
            # or none of them.
            raise ValueError("Unnamed field is not supported by codegen")

        return list(map(lambda r: str(r.name), returns))
