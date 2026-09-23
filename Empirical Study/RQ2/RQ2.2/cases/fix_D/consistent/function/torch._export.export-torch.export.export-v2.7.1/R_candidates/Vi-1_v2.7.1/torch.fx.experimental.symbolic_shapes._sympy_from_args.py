def _sympy_from_args(
    cls: type[Union[sympy.Add, sympy.Mul]],
    args: list[sympy.Expr],
    sort: bool = True,
    is_commutative: Optional[bool] = None,
) -> sympy.Expr:
    if not args:
        return cls.identity  # type: ignore[union-attr]
    # These args are already in canonical form, so we avoid calling
    # Add(*args) to avoid expensive Add.flatten operation
    if sort:
        if cls is sympy.Add:
            sort_fn = sympy.core.add._addsort
        elif cls is sympy.Mul:
            sort_fn = sympy.core.mul._mulsort
        else:
            raise ValueError(f"Unknown cls: {cls}")

        # we don't support non commutative with sort
        assert is_commutative is True
        if args[0].is_Number:
            rest = args[1:]
            sort_fn(rest)
            return cls._from_args([args[0]] + rest, is_commutative=is_commutative)  # type: ignore[attr-defined]
        else:
            args = args.copy()
            sort_fn(args)
            return cls._from_args(args, is_commutative=is_commutative)  # type: ignore[attr-defined]
    else:
        # if the args are already sorted, we create directly
        return cls._from_args(args, is_commutative=is_commutative)  # type: ignore[attr-defined]
