    def _check_setitem_copy(self, stacklevel=4, t='setting', force=False):
        """

        Parameters
        ----------
        stacklevel : integer, default 4
           the level to show of the stack when the error is output
        t : string, the type of setting error
        force : boolean, default False
           if True, then force showing an error

        validate if we are doing a settitem on a chained copy.

        If you call this function, be sure to set the stacklevel such that the
        user will see the error *at the level of setting*

        It is technically possible to figure out that we are setting on
        a copy even WITH a multi-dtyped pandas object. In other words, some
        blocks may be views while other are not. Currently _is_view will ALWAYS
        return False for multi-blocks to avoid having to handle this case.

        df = DataFrame(np.arange(0,9), columns=['count'])
        df['group'] = 'b'

        # This technically need not raise SettingWithCopy if both are view
        # (which is not # generally guaranteed but is usually True.  However,
        # this is in general not a good practice and we recommend using .loc.
        df.iloc[0:5]['group'] = 'a'

        """

        if force or self.is_copy:

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

            # we might be a false positive
            try:
                if self.is_copy().shape == self.shape:
                    self.is_copy = None
                    return
            except:
                pass

            # a custom message
            if isinstance(self.is_copy, string_types):
                t = self.is_copy

            elif t == 'referant':
                t = ("\n"
                     "A value is trying to be set on a copy of a slice from a "
                     "DataFrame\n\n"
                     "See the caveats in the documentation: "
                     "http://pandas.pydata.org/pandas-docs/stable/"
                     "indexing.html#indexing-view-versus-copy"
                     )

            else:
                t = ("\n"
                     "A value is trying to be set on a copy of a slice from a "
                     "DataFrame.\n"
                     "Try using .loc[row_indexer,col_indexer] = value "
                     "instead\n\nSee the caveats in the documentation: "
                     "http://pandas.pydata.org/pandas-docs/stable/"
                     "indexing.html#indexing-view-versus-copy"
                     )

            if value == 'raise':
                raise SettingWithCopyError(t)
            elif value == 'warn':
                warnings.warn(t, SettingWithCopyWarning, stacklevel=stacklevel)
