def _groupby_function(name, alias, npfunc, numeric_only=True,
                      _convert=False):

    _local_template = "Compute %(f)s of group values"

    @Substitution(name='groupby', f=name)
    @Appender(_doc_template)
    @Appender(_local_template)
    def f(self):
        self._set_selection_from_grouper()
        try:
            return self._cython_agg_general(alias, numeric_only=numeric_only)
        except AssertionError as e:
            raise SpecificationError(str(e))
        except Exception:
            result = self.aggregate(lambda x: npfunc(x, axis=self.axis))
            if _convert:
                result = result._convert(datetime=True)
            return result

        f.__name__ = name

    return f
