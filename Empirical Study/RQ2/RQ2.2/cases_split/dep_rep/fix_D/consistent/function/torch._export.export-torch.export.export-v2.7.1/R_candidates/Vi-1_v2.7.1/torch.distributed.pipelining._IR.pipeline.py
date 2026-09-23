def pipeline(
    module: torch.nn.Module,
    mb_args: tuple[Any, ...],
    mb_kwargs: Optional[dict[str, Any]] = None,
    split_spec: Optional[dict[str, SplitPoint]] = None,
    split_policy: Optional[Callable[[fx.GraphModule], fx.GraphModule]] = None,
) -> Pipe:
    """
    Split a module based on a specification.

    See `Pipe` for more details.

    Arguments
    ---------
    module:
        The module to be splitted.
    mb_args:
        Example positional inputs, in micro-batch form.
    mb_kwargs:
        Example keyword inputs, in micro-batch form. (default: `None`)
    split_spec:
        A dictionary using submodule names as split marker. (default: `None`)
    split_policy:
        The policy to use for splitting the module. (default: `None`)

    Returns
    -------
    A pipeline representation of class `Pipe`.
    """
    if split_spec is not None and split_policy is not None:
        raise ValueError(
            "Cannot specify both `split_spec` and `split_policy`. Please use only one of them."
        )

    if split_spec is not None:
        # Annotate split points in the module based on user spec
        annotate_split_points(module, split_spec)
        return Pipe.from_tracing(
            mod=module,
            example_args=mb_args,
            example_kwargs=mb_kwargs,
        )
    else:
        # Use split policy
        return Pipe.from_tracing(
            mod=module,
            example_args=mb_args,
            example_kwargs=mb_kwargs,
            split_policy=split_policy,
        )
