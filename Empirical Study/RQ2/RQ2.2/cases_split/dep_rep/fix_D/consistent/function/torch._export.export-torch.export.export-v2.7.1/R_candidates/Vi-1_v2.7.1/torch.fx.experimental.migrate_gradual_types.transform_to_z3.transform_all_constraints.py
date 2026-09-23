    def transform_all_constraints(traced, counter=0):
        """
        Given a trace, generates constraints and transforms them to z3 format

        """
        dimension_dict = {}  # type: ignore[var-annotated]

        generator = ConstraintGenerator(traced)
        new_constraints, counter = generator.generate_constraints(counter)

        # print(new_constraints.conjucts[0])
        # print(*new_constraints.conjucts, sep='\n')

        # transform precision, matching, consistency till obtaining a fixed point
        new_constraints, counter = iterate_till_fixed_point(new_constraints, counter)
        # print(new_constraints)
        # print(new_constraints.conjucts)
        # new_constraints.conjucts = new_constraints.conjucts[:-1]
        # print(*new_constraints.conjucts, sep='\n')

        transformed, counter = transform_to_z3(new_constraints, counter, dimension_dict)
        # print(transformed)
        return transformed
