def autograd_function_forward_rewritten(original_forward, original_setup_context):
    def new_forward(ctx, *args, **kwargs):
        output = original_forward(*args, **kwargs)
        original_setup_context(ctx, args, output)
        return output

    return new_forward
