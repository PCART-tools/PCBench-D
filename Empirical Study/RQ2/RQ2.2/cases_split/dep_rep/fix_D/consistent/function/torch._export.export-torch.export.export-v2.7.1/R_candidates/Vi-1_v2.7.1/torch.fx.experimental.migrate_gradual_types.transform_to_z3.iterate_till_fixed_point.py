    def iterate_till_fixed_point(constraints, counter):
        """
        Transform constraints till reaching a fixed point
        """
        old_c = None
        while old_c != constraints:
            old_c = constraints
            constraints, counter = transform_constraint(constraints, counter)
        return constraints, counter
