    def evaluate_conditional_with_constraints(
        tracer_root, graph, node, counter=0, user_constraints=None
    ):
        """
        Given an IR and a node representing a conditional, evaluate the conditional
        and its negation
        Args:
            tracer_root: Tracer root for module instances
            node: The node to be evaluated

        Returns: the results of evaluating the condition and the negation with
        the rest of the constraints

        """

        (
            transformed_positive,
            transformed_negative,
        ) = transform_all_constraints_trace_time(tracer_root, graph, node, counter)

        s = z3.Solver()
        s.add(transformed_positive)
        if user_constraints is not None:
            s.add(user_constraints)
        condition = s.check()

        s = z3.Solver()
        s.add(transformed_negative)
        if user_constraints is not None:
            s.add(user_constraints)
        negation = s.check()
        return condition, negation
