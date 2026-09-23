    def _split_drawstyle_linestyle(self, ls):
        '''Split drawstyle from linestyle string

        If `ls` is only a drawstyle default to returning a linestyle
        of '-'.

        Parameters
        ----------
        ls : str
            The linestyle to be processed

        Returns
        -------
        ret_ds : str or None
            If the linestyle string does not contain a drawstyle prefix
            return None, otherwise return it.

        ls : str
            The linestyle with the drawstyle (if any) stripped.
        '''
        ret_ds = None
        for ds in self.drawStyleKeys:  # long names are first in the list
            if ls.startswith(ds):
                ret_ds = ds
                if len(ls) > len(ds):
                    ls = ls[len(ds):]
                else:
                    ls = '-'
                break

        return ret_ds, ls
