    def _check_setitem_copy(self, stacklevel=4, t='setting'):
        """ validate if we are doing a settitem on a chained copy.

        If you call this function, be sure to set the stacklevel such that the
        user will see the error *at the level of setting*"""
        if self.is_copy:

            value = config.get_option('mode.chained_assignment')
            if value is None:
                return

            # see if the copy is not actually refererd; if so, then disolve
            # the copy weakref
            try:
                gc.collect(2)
                if not gc.get_referents(self.is_copy()):
                    self.is_copy = None
                    return
            except:
                pass

            if t == 'referant':
                t = ("A value is trying to be set on a copy of a slice from a "
                     "DataFrame")
            else:
                t = ("A value is trying to be set on a copy of a slice from a "
                     "DataFrame.\nTry using .loc[row_index,col_indexer] = value "
                     "instead")
            if value == 'raise':
                raise SettingWithCopyError(t)
            elif value == 'warn':
                warnings.warn(t, SettingWithCopyWarning, stacklevel=stacklevel)
