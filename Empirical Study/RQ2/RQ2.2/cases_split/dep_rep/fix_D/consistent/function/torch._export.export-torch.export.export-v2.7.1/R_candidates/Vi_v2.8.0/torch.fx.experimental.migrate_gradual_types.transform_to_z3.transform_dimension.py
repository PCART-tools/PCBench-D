    def transform_dimension(dimension, counter, dimension_dict):
        """
        Takes a dimension variable or a number and transforms it to a tuple
        according to our scheme
        Args:
            dimension: The dimension to be transformed
            counter: variable tracking

        Returns:  tuple and the current counter

        """
        if dimension == Dyn:
            counter += 1
            return D(0, z3.Int(counter)), counter
        elif isinstance(dimension, int):
            return D(1, dimension), counter
        elif isinstance(dimension, DVar):
            if dimension.c in dimension_dict:
                return (
                    D(z3.Int(dimension_dict[dimension.c]), z3.Int(dimension.c)),
                    counter,
                )
            else:
                counter += 1
                dimension_dict[dimension.c] = counter
                return D(z3.Int(counter), z3.Int(dimension.c)), counter
