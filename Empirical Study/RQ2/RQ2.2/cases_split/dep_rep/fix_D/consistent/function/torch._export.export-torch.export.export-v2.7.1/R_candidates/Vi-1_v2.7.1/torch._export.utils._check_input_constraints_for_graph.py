def _check_input_constraints_for_graph(
    input_placeholders: list[torch.fx.Node], flat_args_with_path, range_constraints
) -> None:
    def get_keystr(key_path: KeyPath) -> str:
        """For a given index into the flat_args, return a human readable string
        describing how to access it, e.g. "*args["foo"][0].bar"
        """
        # Prefix the keypath with "*args" or "**kwargs" to make it clearer where
        # the arguments come from. Ultimately we ought to serialize the
        # original arg names for the best error message here.
        args_kwargs_key_path = key_path[0]
        assert isinstance(args_kwargs_key_path, SequenceKey)
        if args_kwargs_key_path.idx == 0:
            return f"*args{keystr(key_path[1:])}"
        else:
            kwarg_key = key_path[1]
            assert isinstance(kwarg_key, MappingKey)
            name = str(kwarg_key)[1:-1]  # get rid of the enclosed []
            return f"{name}{keystr(key_path[2:])}"

    import sympy

    from torch._export.passes.add_runtime_assertions_for_constraints_pass import (
        _convert_range_to_int,
    )
    from torch.utils._sympy.solve import try_solve

    if len(flat_args_with_path) != len(input_placeholders):
        raise RuntimeError(
            "Unexpected number of inputs "
            f"(expected {len(input_placeholders)}, got {len(flat_args_with_path)})"
        )
    # NOTE: export already guarantees that the same symbol is used in metadata
    # for all InputDims related by equality constraints, so we can just unify
    # symbols with given input dimension values to check equality constraints.
    unification_map: dict[sympy.Symbol, Any] = {}
    for (key_path, arg), node in zip(flat_args_with_path, input_placeholders):
        node_val = node.meta.get("val")
        if isinstance(node_val, FakeTensor):
            if not isinstance(arg, torch.Tensor):
                raise RuntimeError(
                    f"Expected input at {get_keystr(key_path)} to be a tensor, but got {type(arg)}",
                )

            if len(node_val.shape) != len(arg.shape):
                raise RuntimeError(
                    f"Unexpected number of dimensions in input at {get_keystr(key_path)}.shape "
                    f"(expected {node_val.shape}, got {arg.shape})"
                )

            for j, (arg_dim, node_dim) in enumerate(zip(arg.shape, node_val.shape)):
                if (
                    isinstance(arg_dim, torch.SymInt)
                    and not arg_dim.node.expr.is_number
                ):
                    # This can happen when, say, arg is a fake tensor.
                    # We do not run checks on symbolic shapes of fake inputs as
                    # such checks can affect the shape env.
                    continue
                if (
                    isinstance(node_dim, torch.SymInt)
                    and len(node_dim.node.expr.free_symbols) == 1
                ):
                    symbol = next(iter(node_dim.node.expr.free_symbols))
                    if symbol in unification_map:
                        existing_dim = node_dim.node.expr.subs(unification_map)
                        if arg_dim != existing_dim:
                            raise RuntimeError(
                                f"Expected input at {get_keystr(key_path)}.shape[{j}] to be equal to "
                                f"{existing_dim}, but got {arg_dim}",
                            )
                    else:
                        if isinstance(node_dim.node.expr, sympy.Symbol):
                            # Short cut for try_solve below. Also useful in cases where
                            # sympy.Eq(node_dim.node.expr, arg_dim) would evaluate to False
                            # purely because symbol is constrained to be size-like,
                            # e.g., when node_dim.node.expr = symbol and arg_dim = 0.
                            unification_map[symbol] = int(arg_dim)
                        else:
                            solution = try_solve(
                                sympy.Eq(node_dim.node.expr, arg_dim), symbol
                            )
                            if solution is None:
                                raise RuntimeError(  # noqa: B904
                                    f"Expected input {node.name}.shape[{j}] = {arg_dim} to be "
                                    f"of the form {node_dim.node.expr}, where {symbol} is an integer"
                                )
                            else:
                                unification_map[symbol] = int(solution[1])

                    if node_dim.node.expr in range_constraints:
                        min_val, max_val = _convert_range_to_int(
                            range_constraints[node_dim.node.expr]
                        )
                        # NOTE: we allow dimensions to be 0/1 at runtime
                        if min_val > 2:
                            if arg_dim < min_val:
                                raise RuntimeError(
                                    f"Expected input at {get_keystr(key_path)}.shape[{j}] to be >= "
                                    f"{min_val}, but got {arg_dim}",
                                )
                        if max_val < math.inf:
                            if arg_dim > max_val:
                                raise RuntimeError(
                                    f"Expected input at {get_keystr(key_path)}.shape[{j}] to be <= "
                                    f"{max_val}, but got {arg_dim}",
                                )
                elif (
                    isinstance(node_dim, torch.SymInt)
                    and not node_dim.node.expr.is_number
                ):
                    # this means we deferred a guard from export analysis to runtime, let this pass
                    # we'll add a runtime assert checking equality to this replacement expression
                    continue
                elif arg_dim != node_dim:
                    raise RuntimeError(
                        f"Expected input at {get_keystr(key_path)}.shape[{j}] to be equal to "
                        f"{node_dim}, but got {arg_dim}",
                    )
        elif isinstance(node_val, (int, float, str)):
            if type(arg) != type(node_val) or arg != node_val:
                raise RuntimeError(
                    f"Expected input at {get_keystr(key_path)} to be equal to {node_val}, but got {arg}",
                )
