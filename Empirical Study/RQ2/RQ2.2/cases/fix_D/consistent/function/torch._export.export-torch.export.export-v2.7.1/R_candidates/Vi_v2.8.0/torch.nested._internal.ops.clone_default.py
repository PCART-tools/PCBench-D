@register_jagged_func(
    torch.ops.aten.clone.default, "input: jt_all, memory_format: any?"
)
def clone_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")

    new_meta = extract_kwargs(inp)

    if inp._lengths is not None:
        if new_kwargs["memory_format"] == torch.contiguous_format:
            # need to copy to remove "holes" non-contiguity / lengths metadata
            # TODO: write a kernel for this
            from .nested_tensor import jagged_from_list

            # TODO: We probably want the output to have the same ragged structure / nested int.
            assert inp._ragged_idx == 1, (
                "NJT with ragged_idx != 1 not supported for contiguous clone"
            )
            contig, _ = jagged_from_list(inp.unbind(), offsets=None)
            return contig

    return NestedTensor(func(inp._values, **new_kwargs), **new_meta)
