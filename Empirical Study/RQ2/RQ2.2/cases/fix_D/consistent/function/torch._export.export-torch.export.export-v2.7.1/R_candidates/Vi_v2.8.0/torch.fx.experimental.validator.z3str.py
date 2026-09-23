    def z3str(e: z3.ExprRef) -> str:
        assert z3.is_expr(e), f"unsupported expression type: {e}"

        def get_args_str(e: z3.ExprRef) -> list[str]:
            return [z3str(e.arg(i)) for i in range(e.num_args())]

        # First, we simplify the given expression.
        # This is done using rewriting rules, so shouldn't take long.
        e = z3.simplify(e)

        # Only support function applications.
        # Even Z3 "variables" are, in fact, function applications.
        if not z3.is_app(e):
            raise ValueError(f"can't print Z3 expression: {e}")

        if z3.is_int_value(e) or z3.is_rational_value(e):
            return e.as_string()  # type: ignore[attr-defined]

        decl = e.decl()
        kind = decl.kind()
        op = str(decl)
        args = get_args_str(e)

        if kind == z3.Z3_OP_POWER:
            op = "pow"

        elif kind in (z3.Z3_OP_ADD, z3.Z3_OP_MUL):
            # Collect the arguments of chains of ADD and MUL.
            # This is safe, since they are associative.

            def collect_str_args(e):
                if not (z3.is_app(e) and e.decl().kind() == kind):
                    return [z3str(e)]
                else:
                    return [
                        x
                        for i in range(e.num_args())
                        for x in collect_str_args(e.arg(i))
                    ]

            args = collect_str_args(e)

        elif kind == z3.Z3_OP_NOT:
            # Revert some conversions that z3.simplify applies:
            #   - a != b ==> (Not (== a b)) ==> (!= a b)
            #   - a < b ==> (Not (<= b a)) ==> (> b a)
            #   - a > b ==> (Not (<= a b)) ==> (> a b)

            assert e.num_args() == 1
            arg = e.arg(0)

            assert z3.is_app(arg)
            argkind = arg.decl().kind()

            logic_inverse = {
                z3.Z3_OP_EQ: "!=",
                z3.Z3_OP_LE: ">",
                z3.Z3_OP_GE: "<",
            }

            if argkind in logic_inverse:
                op = logic_inverse[argkind]
                args = get_args_str(arg)

        elif kind in (z3.Z3_OP_TO_INT, z3.Z3_OP_TO_REAL):
            assert e.num_args() == 1
            argstr = z3str(e.arg(0))

            # Check if it's the floor division pattern.
            if argstr.startswith("(/"):
                return "(idiv" + argstr[2:]

            # Otherwise, just ignore it.
            return argstr

        elif kind == z3.Z3_OP_UNINTERPRETED:
            assert e.num_args() == 0
            return str(decl)

        string = op + " " + " ".join(args)
        return f"({string.rstrip()})"
