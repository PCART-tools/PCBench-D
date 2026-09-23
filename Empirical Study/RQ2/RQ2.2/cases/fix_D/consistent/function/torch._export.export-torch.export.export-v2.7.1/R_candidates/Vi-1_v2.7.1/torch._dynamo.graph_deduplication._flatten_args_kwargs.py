def _flatten_args_kwargs(args: Any) -> list[Node]:
    fully_flattened = []

    def flatten(args: Any) -> None:
        flattened, _ = tree_flatten(args)
        for arg in flattened:
            if isinstance(arg, slice):
                start = arg.start
                stop = arg.stop
                step = arg.step
                flatten((start, stop, step))
            else:
                fully_flattened.append(arg)

    flatten(args)

    return fully_flattened
