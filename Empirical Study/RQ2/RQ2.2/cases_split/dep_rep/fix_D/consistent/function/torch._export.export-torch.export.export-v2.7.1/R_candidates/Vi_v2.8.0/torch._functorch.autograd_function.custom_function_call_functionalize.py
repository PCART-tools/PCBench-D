@custom_function_call.py_impl(TransformType.Functionalize)
def custom_function_call_functionalize(
    interpreter, autograd_function, generate_vmap_rule, *operands
):
    raise RuntimeError("NYI: Functionalize rule for custom_function_call")
