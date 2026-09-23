    def z3op(op: Callable, validator: "TranslationValidator") -> Callable:
        # Operations that have booleans as their argument.
        # This is needed because the argument of some FX nodes were
        # literal integers, instead of booleans. So, whenever this flag
        # is set, we also convert ints to booleans.
        boolean_ops = {operator.not_}
        as_bool = op in boolean_ops

        # Lifts the function into 'z3.ExprRef' domain.
        def lift(func):
            def wrap(a) -> z3.ExprRef:
                if isinstance(a, (z3.ArithRef, z3.BoolRef)):
                    return a
                # Convert it into a Z3 value, if it is some of the supported
                # types below.
                if isinstance(a, bool) or (as_bool and isinstance(a, int)):
                    return z3.BoolVal(bool(a))
                if isinstance(a, (int, sympy.Integer)):
                    return z3.IntVal(int(a))
                if isinstance(a, (float, sympy.Float)):
                    return z3.RealVal(float(a))
                raise ValueError(f"can't lift type: {type(a)}")

            @functools.wraps(func)
            def wrapper(*args):
                # Lifts the arguments into a list of Z3 inhabitants.
                if len(args) == 1 and isinstance(args[0], (list, tuple)):
                    wrapped_args = (tuple(wrap(a) for a in args[0]),)
                else:
                    wrapped_args = tuple(wrap(a) for a in args)
                # Run the function on the Z3 expressions.
                return func(*wrapped_args)

            return wrapper

        ops = _Z3Ops(validator)
        replacement_map = {
            # Operator module.
            operator.not_: lift(z3.Not),
            operator.and_: lift(ops.bitwise_and),
            operator.or_: lift(ops.bitwise_or),
            operator.lshift: lift(ops.lshift),
            operator.rshift: lift(ops.rshift),
            operator.floordiv: lift(ops.floordiv),
            operator.truediv: lift(ops.div),
            operator.mod: lift(ops.mod),
            operator.abs: lift(ops.abs),
            builtins.round: lift(ops.round_to_int),
            # Math module.
            math.ceil: lift(ops.ceil),
            math.floor: lift(ops.floor),
            math.trunc: lift(ops.trunc),
            # Torch module.
            torch.sym_float: lift(ops.to_real),
            torch.sym_max: lift(ops.max),
            torch.sym_min: lift(ops.min),
            torch.sym_sum: lift(ops.sym_sum),
            torch.sym_ite: lift(lambda b, t, f: t if b else f),
            torch._sym_sqrt: lift(ops.sqrt),  # type: ignore[attr-defined]
            # Not lifted because we only use this function as a
            # marker for adding the expression as validator input.
            torch._assert: torch._assert,
        }
        return replacement_map[op] if op in replacement_map else lift(op)
