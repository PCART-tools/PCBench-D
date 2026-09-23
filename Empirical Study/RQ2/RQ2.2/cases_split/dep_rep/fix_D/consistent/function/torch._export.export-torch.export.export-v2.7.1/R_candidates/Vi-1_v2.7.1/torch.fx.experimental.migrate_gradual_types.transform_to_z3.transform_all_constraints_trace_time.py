    def transform_all_constraints_trace_time(tracer_root, graph, node, counter=0):
        """
        Takes a node and a graph and generates two sets of constraints.
        One set constraints the node's constraints and another set
        constraints the negation of the node's constraints
        Args:
            tracer_root: the root for getting the module instances
            graph: the graph so far in the tracing process
            node: node that represents a conditional
            counter: variable tracking

        Returns: Two sets of constraints. One with a conjunction with the
        the conditional constraint and the other with a conjunction with
        its negation.

        """
        dimension_dict = {}  # type: ignore[var-annotated]

        generator = ConstraintGenerator(tracer_root, graph)
        new_constraints, counter = generator.generate_constraints(counter)

        condition_constraint = new_constraints.conjucts[-1]

        # we know the constraint is a conjunction where the last constraint is about the conditional
        # so remove the last constraint
        new_constraints.conjucts = new_constraints.conjucts[:-1]

        # transform precision, matching, consistency till obtaining a fixed point
        new_constraints, counter = iterate_till_fixed_point(new_constraints, counter)

        # since the function returns a list of one element, we get the first element
        # we are only interested in the RHS in this case because the LHS just stores
        # the result

        # we make sure the constraint is of the form:
        # c = b where b is a boolean expression
        # and we consider b (constraint.rhs) for transformation
        assert isinstance(condition_constraint.lhs, BVar)
        assert is_bool_expr(condition_constraint.rhs)
        condition_constraint_rhs = condition_constraint.rhs

        # transform the condition constraint
        condition_constraint_rhs, counter = iterate_till_fixed_point(
            condition_constraint_rhs, counter
        )

        transformed, counter = transform_to_z3(new_constraints, counter, dimension_dict)

        transformed_condition_constraint, counter = transform_to_z3(
            condition_constraint_rhs, counter, dimension_dict
        )

        negation_transformed_condition_constraint = z3.Not(
            transformed_condition_constraint
        )

        return z3.And([transformed, transformed_condition_constraint]), z3.And(
            [transformed, negation_transformed_condition_constraint]
        )
