@register_jagged_func(
    torch.ops.aten.embedding_dense_backward.default,
    "grad_output: jt, indices: jt, num_weights: any, padding_idx: any, scale_grad_by_freq: any",
)
def embedding_dense_backward_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    indices = new_kwargs.pop("indices")
    grad_output = new_kwargs.pop("grad_output")
    return func(grad_output._values, indices._values, **new_kwargs)
