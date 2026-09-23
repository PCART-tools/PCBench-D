def emit_single_dispatch(
    ps: PythonSignature, f: NativeFunction, namedtuple_typenames: Dict[str, str]
) -> str:
    """
    Emit dispatch code for a single native function.
    """
    @with_native_function
    def go(f: NativeFunction) -> str:
        # header comments
        deprecated = '[deprecated] ' if ps.deprecated else ''
        schema_comment = f'// {deprecated}aten::{f.func}'

        # dispatch lambda signature
        name = cpp.name(f.func)
        lambda_formals = ', '.join(map(lambda a: f"{a.type_str} {a.name}",
                                       dispatch_lambda_args(ps, f)))
        lambda_return = dispatch_lambda_return_str(f)

        # dispatch lambda body
        dispatch_callee = cpp_dispatch_target(f)
        dispatch_args = ', '.join(cpp_dispatch_exprs(f, python_signature=ps))

        # from arg parser outputs to dispatch lambda arguments
        parser_outputs = arg_parser_output_exprs(ps, f)
        lambda_arg_exprs = dispatch_lambda_exprs(ps, f)
        inits = '\n'.join(lambda_arg_exprs.inits)
        lambda_args = ', '.join(lambda_arg_exprs.exprs)

        # scatter fields
        # TODO: Checking `ps.method and ('requires_grad' in parser_outputs)` is a hacky
        #       solution for enabling the 'requires_grad' argument for tensor methods
        #       new_full, new_empty, and new_zeros. A much better but more difficult to
        #       implement solution involves refactoring according to Ed's description here:
        #       https://github.com/pytorch/pytorch/issues/36455#issuecomment-614767589
        need_set_requires_grad = ps.tensor_options_args and (not has_tensor_options(f) or (
            ps.method and ('requires_grad' in parser_outputs)))
        set_requires_grad = f'.set_requires_grad({parser_outputs["requires_grad"].expr})' \
            if need_set_requires_grad else ''

        if lambda_return == 'void':
            return f"""\
{schema_comment}
{inits}
auto dispatch_{name} = []({lambda_formals}) -> {lambda_return} {{
  pybind11::gil_scoped_release no_gil;
  {dispatch_callee}({dispatch_args});
}};
dispatch_{name}({lambda_args}){set_requires_grad};
Py_RETURN_NONE;
"""
        else:
            typename = namedtuple_typenames.get(gen_namedtuple_typename_key(f))
            namedtuple_typeref = f'{typename}, ' if typename is not None else ''
            return f"""\
{schema_comment}
{inits}
auto dispatch_{name} = []({lambda_formals}) -> {lambda_return} {{
  pybind11::gil_scoped_release no_gil;
  return {dispatch_callee}({dispatch_args});
}};
return wrap({namedtuple_typeref}dispatch_{name}({lambda_args}){set_requires_grad});
"""

    return go(f)
