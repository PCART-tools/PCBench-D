    def _deprecated(self, op):
        warnings.warn(("\n.resample() is now a deferred operation\n"
                       "You called {op}(...) on this deferred object "
                       "which materialized it into a {klass}\nby implicitly "
                       "taking the mean.  Use .resample(...).mean() "
                       "instead").format(op=op, klass=self._typ),
                      FutureWarning, stacklevel=3)
        return self.mean()
