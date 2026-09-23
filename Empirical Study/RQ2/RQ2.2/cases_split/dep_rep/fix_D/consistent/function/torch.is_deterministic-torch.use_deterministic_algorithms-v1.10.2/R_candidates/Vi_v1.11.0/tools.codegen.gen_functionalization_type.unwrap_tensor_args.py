def unwrap_tensor_args(sig: DispatcherSignature) -> Tuple[str, List[Binding]]:
    context: List[Binding] = []
    unwrapped_tensor_args: List[str] = []
    for arg in sig.arguments():
        if is_tensor_like(arg.argument):
            # for tensor inputs, we want to unwrap them before passing them into the redispatch calls.
            unwrapped_name = f'{arg.name}_'
            unwrapped_tensor_args.append(
                f'auto {unwrapped_name} = at::functionalization::impl::from_functional_tensor({arg.name});')
            context.append(arg.with_name(unwrapped_name))
        else:
            # for non-tensor inputs, we want to pass them directly into the redispatch calls.
            context.append(arg)
    unwrap_tensor_args_str = '\n      '.join(unwrapped_tensor_args)
    return unwrap_tensor_args_str, context
