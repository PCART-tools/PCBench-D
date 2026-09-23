    def transform_algebraic_expression(expr, counter, dimension_dict):
        """
        Transforms an algebraic expression to z3 format
        Args:
            expr: An expression is either a dimension variable or an algebraic-expression


        Returns: the transformed expression

        """
        assert is_algebraic_expression(expr) or is_dim(expr)

        if is_dim(expr):
            transformed, counter = transform_dimension(expr, counter, dimension_dict)
            return transformed.arg(1), counter

        elif isinstance(expr, Prod):
            dims = []
            for dim in expr.products:
                assert is_dim(dim)
                d, counter = transform_dimension(dim, counter, dimension_dict)
                dims.append(d.arg(1))
            return z3.Product(dims), counter

        elif is_algebraic_expression(expr):
            lhs, counter = transform_algebraic_expression(
                expr.lhs, counter, dimension_dict
            )
            rhs, counter = transform_algebraic_expression(
                expr.rhs, counter, dimension_dict
            )

            if expr.op == op_sub:
                c = lhs - rhs

            elif expr.op == op_add:
                c = lhs + rhs

            elif expr.op == op_div:
                c = lhs / rhs

            elif expr.op == op_mul:
                c = lhs * rhs

            elif expr.op == op_mod:
                c = lhs % rhs

            else:
                raise NotImplementedError("operation not yet implemented")

            return c, counter

        else:
            raise RuntimeError
