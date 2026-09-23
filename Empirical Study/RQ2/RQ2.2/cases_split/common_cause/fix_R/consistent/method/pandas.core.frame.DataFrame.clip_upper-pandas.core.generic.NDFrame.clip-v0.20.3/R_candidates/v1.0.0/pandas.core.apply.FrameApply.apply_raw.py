    def apply_raw(self):
        """ apply to the values as a numpy array """
        try:
            result = libreduction.compute_reduction(self.values, self.f, axis=self.axis)
        except ValueError as err:
            if "Function does not reduce" not in str(err):
                # catch only ValueError raised intentionally in libreduction
                raise
            # We expect np.apply_along_axis to give a two-dimensional result, or
            #  also raise.
            result = np.apply_along_axis(self.f, self.axis, self.values)

        # TODO: mixed type case
        if result.ndim == 2:
            return self.obj._constructor(result, index=self.index, columns=self.columns)
        else:
            return self.obj._constructor_sliced(result, index=self.agg_axis)
