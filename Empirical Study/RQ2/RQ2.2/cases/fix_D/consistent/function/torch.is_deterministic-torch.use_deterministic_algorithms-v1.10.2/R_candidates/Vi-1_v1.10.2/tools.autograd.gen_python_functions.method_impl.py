def method_impl(
    name: BaseOperatorName,
    module: Optional[str],
    overloads: Sequence[PythonSignatureNativeFunctionPair],
    *,
    method: bool
) -> str:
    """
    Generate a python binding for all overloads of an op.
    """
    pycname = get_pycname(name)
    noarg = is_noarg(overloads)
    namedtuple_inits, namedtuple_typenames = emit_namedtuple_typedefs(overloads)

    method_header = ['HANDLE_TH_ERRORS']
    method_header += namedtuple_inits
    method_header += [
        "const Tensor& self = THPVariable_Unpack(self_);"
    ] if method else []

    method_footer = ([] if noarg else ['Py_RETURN_NONE;']) + ['END_HANDLE_TH_ERRORS']

    traceable = 'true' if all(should_trace(o.function) for o in overloads) else 'false'

    grouped_overloads: Sequence[PythonSignatureGroup] = group_overloads(overloads)
    is_singleton = len(grouped_overloads) == 1
    signatures: List[str] = []
    dispatch: List[str] = []
    for overload_index, overload in enumerate(grouped_overloads):
        signature = overload.signature.signature_str()
        signatures.append(f'{cpp_string(str(signature))},')
        dispatch_body = emit_dispatch_case(overload, namedtuple_typenames)
        dispatch.append(
            PY_VARIABLE_CASE.substitute(overload_index=overload_index, body=dispatch_body)
            if not is_singleton else dispatch_body)

    if noarg:
        template = PY_VARIABLE_METHOD_NOARGS
    elif is_singleton:
        template = PY_VARIABLE_METHOD_VARARGS_SINGLETON
    else:
        template = PY_VARIABLE_METHOD_VARARGS

    return template.substitute(
        name=name,
        pycname=pycname,
        method_header=method_header,
        max_args=max(map(lambda o: o.signature.arguments_count(), overloads)),
        signatures=signatures,
        traceable=traceable,
        check_has_torch_function=gen_has_torch_function_check(
            name=name,
            module=module,
            noarg=noarg,
            method=method,
        ),
        dispatch=dispatch,
        method_footer=method_footer,
        self_="self_" if method else "nullptr",
    )
