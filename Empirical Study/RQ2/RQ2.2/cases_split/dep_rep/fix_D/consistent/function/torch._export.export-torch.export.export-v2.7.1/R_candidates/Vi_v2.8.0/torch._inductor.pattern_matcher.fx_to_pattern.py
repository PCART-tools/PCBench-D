def fx_to_pattern(
    gm: Union[torch.fx.GraphModule, torch.fx.Graph],
    ignore_types: Sequence[type[Any]] = (),
    argnames: Sequence[str] = (),
    scalar_workaround: Union[dict[str, Union[float, int]], None] = None,
    exclusive_arg_names: Sequence[str] = (),
) -> PatternExpr:
    """
    Convert an FX graph into a PatternExpr.  This is useful for simple
    patterns that can only match single functions and fixed-length lists.
    """
    # scalar_workaround is a hack to capture dropout_p
    # see https://github.com/pytorch/pytorch/issues/97894
    scalar_workaround = scalar_workaround or {}
    inv_scalar_workaround = {v: k for k, v in scalar_workaround.items()}
    assert len(inv_scalar_workaround) == len(scalar_workaround)

    def process_arg(
        x: T, ignore_types_override: Optional[Sequence[type[Any]]] = None
    ) -> Union[T, KeywordArg, Ignored]:
        current_ignore_types = (
            ignore_types_override if ignore_types_override is not None else ignore_types
        )
        if isinstance(x, (float, int)) and x in inv_scalar_workaround:
            return KeywordArg(inv_scalar_workaround[x])
        if type(x) in current_ignore_types:
            return Ignored()
        if isinstance(x, list) and all(isinstance(y, Ignored) for y in x) and x:
            return Ignored()
        return x

    argnum = itertools.count()

    class Converter(torch.fx.Interpreter):
        call_method = _not_implemented
        call_module = _not_implemented
        get_attr = _not_implemented

        def placeholder(
            self,
            target: str,  # type: ignore[override]
            args: Sequence[Any],
            kwargs: Mapping[str, Any],
        ) -> Union[ExclusiveKeywordArg, KeywordArg]:
            n = next(argnum)
            if n < len(argnames):
                name = argnames[n]
            elif argnames:
                assert target.startswith("tangent")
                name = target
            else:
                target = re.sub(r"_\d+$", "", target)  # de-mangle arg name
                name = target
            if name in exclusive_arg_names:
                return ExclusiveKeywordArg(name)
            else:
                return KeywordArg(name)

        def call_function(
            self,
            target: str,  # type: ignore[override]
            args: Sequence[Any],
            kwargs: Mapping[str, Any],
        ) -> PatternExpr:
            process_arg_fn = process_arg
            # Indexing is critical for matching getitem nodes, so we can't ignore int args here
            if target == operator.getitem:

                def process_arg_fn_impl(
                    x: T,
                    ignore_types_override: Optional[Sequence[type[Any]]] = tuple(
                        t for t in ignore_types if t is not int
                    ),
                ) -> Union[T, KeywordArg, Ignored]:
                    return process_arg(x, ignore_types_override)

                process_arg_fn = process_arg_fn_impl

            args, kwargs = pytree.tree_map(process_arg_fn, (args, kwargs))
            if list in ignore_types:
                # Handle a burned in tensor size which are now [Ignored(), Ignored(), ...]
                args = [process_arg_fn(a) for a in args]
                kwargs = {k: process_arg_fn(a) for k, a in kwargs.items()}
            return CallFunction(target, *args, **kwargs)

        def run_node(self, n: torch.fx.Node) -> Any:
            rv = super().run_node(n)
            if n.op == "output" and isinstance(rv, tuple):
                args = n.args[0]
                assert isinstance(args, Collection)
                assert len(rv) == len(args)
                for r, arg in zip(rv, args):
                    r.users = len(arg.users)
            else:
                rv.users = len(n.users)
            return rv

    assert isinstance(gm, torch.fx.GraphModule)
    pattern = Converter(gm).run()
    if not isinstance(pattern, PatternExpr):
        return MultiOutputPattern(pytree.tree_leaves(pattern))
    return pattern
