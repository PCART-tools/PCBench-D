    def fillna(self, value, limit=None, inplace=False, downcast=None,
               mgr=None):
        # we may need to upcast our fill to match our dtype
        if limit is not None:
            raise NotImplementedError("specifying a limit for 'fillna' has "
                                      "not been implemented yet")

        values = self.values if inplace else self.values.copy()
        values = self._try_coerce_result(values.fillna(value=value,
                                                       limit=limit))
        return [self.make_block(values=values)]
