def method_def(
    name: BaseOperatorName,
    module: Optional[str],
    overloads: Sequence[PythonSignatureNativeFunctionPair],
    *,
    method: bool
) -> str:
    """
    Generate method def entry.
    """
    pycname = get_pycname(name)

    if is_noarg(overloads):
        pyfunc_cast = ''
        flags = 'METH_NOARGS' if method else 'METH_VARARGS | METH_KEYWORDS'
    else:
        pyfunc_cast = 'castPyCFunctionWithKeywords'
        flags = 'METH_VARARGS | METH_KEYWORDS'

    if module == "torch":
        flags += ' | METH_STATIC'

    if name.dunder_method:
        # PyMethodDef entry for binary op, throws not implemented error
        return f"""\
{{"{name}", {pyfunc_cast}(TypeError_to_NotImplemented_<{pycname}>), {flags}, NULL}},"""
    else:
        # PyMethodDef entry
        return f"""\
{{"{name}", {pyfunc_cast}({pycname}), {flags}, NULL}},"""
