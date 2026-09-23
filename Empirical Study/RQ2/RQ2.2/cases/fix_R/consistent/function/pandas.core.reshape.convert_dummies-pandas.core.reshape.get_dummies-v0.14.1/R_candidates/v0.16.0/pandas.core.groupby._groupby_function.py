def _groupby_function(name, alias, npfunc, numeric_only=True,
                      _convert=False):
    def f(self):
        self._set_selection_from_grouper()
        try:
            return self._cython_agg_general(alias, numeric_only=numeric_only)
        except AssertionError as e:
            raise SpecificationError(str(e))
        except Exception:
            result = self.aggregate(lambda x: npfunc(x, axis=self.axis))
            if _convert:
                result = result.convert_objects()
            return result

    f.__doc__ = "Compute %s of group values" % name
    f.__name__ = name

    return f
