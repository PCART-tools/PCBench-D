    def evaluate(self):
        """Run the engine on the expression

        This method performs alignment which is necessary no matter what engine
        is being used, thus its implementation is in the base class.

        Returns
        -------
        obj : object
            The result of the passed expression.
        """
        if not self._is_aligned:
            self.result_type, self.aligned_axes = _align(self.expr.terms)

        # make sure no names in resolvers and locals/globals clash
        res = self._evaluate()
        return _reconstruct_object(self.result_type, res, self.aligned_axes,
                                   self.expr.terms.return_type)
