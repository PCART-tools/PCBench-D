def _free_unbacked_symbols_with_path(
    a: object,
    path: pytree.KeyPath,
    real: Optional[object] = None,
    shape_env: Optional[ShapeEnv] = None,
    pending: Optional[set[sympy.Symbol]] = None,
    simplify: bool = False,
) -> dict[sympy.Symbol, pytree.KeyPath]:
    go = functools.partial(
        _free_unbacked_symbols_with_path,
        shape_env=shape_env,
        pending=pending,
        simplify=simplify,
    )

    def expr(s: Union[SymInt, SymFloat, SymBool]) -> sympy.Expr:
        if simplify:
            return s.node.expr
        # (When called from compute_unbacked_bindings)
        # NB: Intentionally access _expr, not expr, do not want
        # simplification!
        return s.node._expr

    if pending is None:
        pending = set()
    r = {}
    if isinstance(a, (tuple, list)):
        # NB: real is apparently not always a tuple/list here
        # python test/inductor/test_torchinductor.py CpuTests.test_index_propagation_nested_indirect_indexing_cpu
        for i in range(len(a)):
            r.update(
                go(
                    a[i],
                    path + (pytree.SequenceKey(i),),
                    real=real[i] if real is not None else None,  # type: ignore[index]
                )
            )
    elif is_traceable_wrapper_subclass(a):
        # TODO: Determine if this is correct
        attrs, _ = a.__tensor_flatten__()
        for attr in attrs:
            sub = getattr(a, attr)
            r.update(go(sub, path + (InnerTensorKey(attr),)))
    elif isinstance(a, torch.Tensor):
        from torch._subclasses.fake_tensor import FakeTensor

        assert isinstance(a, FakeTensor)
        r.update(
            go(
                a.size(),
                path + (CallMethodKey("size"),),
                real=a.real_tensor.size() if a.real_tensor is not None else None,
            )
        )
        if a.layout not in [
            torch.sparse_csr,
            torch.sparse_csc,
            torch.sparse_bsr,
            torch.sparse_bsc,
        ]:
            r.update(
                go(
                    a.stride(),
                    path + (CallMethodKey("stride"),),
                    real=a.real_tensor.stride() if a.real_tensor is not None else None,
                )
            )
        r.update(
            go(
                a.storage_offset(),
                path + (CallMethodKey("storage_offset"),),
                real=(
                    a.real_tensor.storage_offset()
                    if a.real_tensor is not None
                    else None
                ),
            )
        )

    elif (
        isinstance(a, (torch.SymInt, torch.SymFloat))
        and isinstance(s := expr(a), sympy.Symbol)
        and s in pending
    ):
        r[s] = path
        if shape_env and real is not None:
            assert isinstance(real, (int, float))
            shape_env.set_unbacked_var_to_val(s, real)
        pending.remove(s)
    # When an unbacked SymInt is perfectly divisible by an integer
    # constant, we replace it with the integer constant to improve
    # reasoning capabilities.  However, in synthetic examples, it is
    # then possible that the factor never is explicitly allocated.
    # Fortunately, we can compute it by division.
    elif (
        isinstance(a, torch.SymInt)
        and isinstance(s := expr(a), sympy.Mul)
        and len(s.args) == 2
        and isinstance(lhs := s.args[0], (sympy.Integer, sympy.Symbol))
        and isinstance(rhs := s.args[1], sympy.Symbol)
        # support exactly one unbacked for now
        and ((rhs in pending) ^ (lhs in pending))
        # support constant coefficient or backed symbolic coefficient
        and (
            isinstance(coeff := lhs if lhs not in pending else rhs, sympy.Integer)
            or shape_env
            and coeff in shape_env.var_to_val
        )
    ):

        def _symint_wrap(s: sympy.Symbol) -> SymInt:
            return shape_env.create_symintnode(  # type: ignore[union-attr]
                s,
                hint=int(shape_env.var_to_val[s]),  # type: ignore[union-attr]
                source=shape_env.var_to_sources.get(s, [None])[0],  # type: ignore[union-attr]
            )

        unbacked = lhs if lhs in pending else rhs
        divisor: Union[int, SymInt] = (
            int(coeff)
            if shape_env and isinstance(coeff, sympy.Integer)
            else _symint_wrap(coeff)
        )
        # TODO: DivideByKey needs to test divisibility at runtime!
        r[unbacked] = path + (DivideByKey(divisor),)
        if real is not None:
            assert isinstance(real, int)
            val = (
                real // int(coeff)
                if isinstance(coeff, sympy.Integer)
                else CleanDiv(real, coeff)
            )
            if shape_env:
                shape_env.set_unbacked_var_to_val(unbacked, val)
        pending.remove(unbacked)
    # The annoyance here arises from the fact that SymBool is
    # allocated by allocating a SymInt and then testing if it's equal
    # to one.  So you have a complicated binding site logic for this.
    elif (
        isinstance(a, torch.SymBool)
        and isinstance(s := expr(a), sympy.Eq)
        # This must match create_unbacked_symbool EXACTLY
        and isinstance(s.lhs, sympy.Symbol)
        and s.rhs == 1
        and s.lhs in pending
    ):
        r[s.lhs] = path + (ConvertIntKey(),)
        if real is not None:
            assert type(real) is bool
            if shape_env:
                shape_env.set_unbacked_var_to_val(s, int(real))
        pending.remove(s.lhs)

    return r
