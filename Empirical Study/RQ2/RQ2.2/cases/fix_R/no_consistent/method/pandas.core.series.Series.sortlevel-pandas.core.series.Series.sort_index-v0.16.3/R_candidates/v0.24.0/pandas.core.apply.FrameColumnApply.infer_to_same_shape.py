    def infer_to_same_shape(self):
        """ infer the results to the same shape as the input object """
        results = self.results

        result = self.obj._constructor(data=results)
        result = result.T

        # set the index
        result.index = self.res_index

        # infer dtypes
        result = result.infer_objects()

        return result
