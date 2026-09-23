@custom_function_call.py_impl(TransformType.Grad)
@custom_function_call.py_impl(TransformType.Jvp)
def custom_function_call_grad(interpreter, autograd_function, *operands):
    Generated = generate_single_level_function(interpreter, autograd_function)
    with enable_single_level_autograd_function():
        flat_out = Generated.apply(*operands)
    return flat_out
