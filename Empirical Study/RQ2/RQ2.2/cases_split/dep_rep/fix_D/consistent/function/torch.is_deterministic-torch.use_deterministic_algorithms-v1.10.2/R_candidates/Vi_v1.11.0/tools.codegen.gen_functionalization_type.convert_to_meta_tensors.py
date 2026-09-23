def convert_to_meta_tensors(sig: DispatcherSignature) -> Tuple[str, List[Binding]]:
    context: List[Binding] = []
    unwrapped_tensor_args: List[str] = []
    for arg in sig.arguments():
        if is_tensor_like(arg.argument):
            # for tensor inputs, we want to unwrap them before passing them into the redispatch calls.
            # for tensor inputs, we want to unwrap them before passing them into the redispatch calls.
            a_ = arg.name
            unwrapped_name = f'{arg.name}_meta'
            unwrapped_tensor_args.append(
                f"auto {unwrapped_name} = at::native::empty_strided_meta({a_}.sizes(), {a_}.strides(), \
/*dtype=*/c10::make_optional({a_}.scalar_type()), /*layout=*/c10::make_optional({a_}.layout()), \
/*device=*/c10::make_optional(c10::Device(kMeta)), /*pin_memory=*/c10::nullopt);"
            )
            context.append(arg.with_name(unwrapped_name))
        else:
            # for non-tensor inputs, we want to pass them directly into the redispatch calls.
            context.append(arg)
    unwrap_tensor_args_str = '\n        '.join(unwrapped_tensor_args)
    return unwrap_tensor_args_str, context
