    def _split_drawstyle_linestyle(self, ls):
        """
        Split drawstyle from linestyle string.

        If *ls* is only a drawstyle default to returning a linestyle
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
        """
        for ds in self.drawStyleKeys:  # long names are first in the list
            if ls.startswith(ds):
                cbook.warn_deprecated(
                    "3.1", message="Passing the drawstyle with the linestyle "
                    "as a single string is deprecated since Matplotlib "
                    "%(since)s and support will be removed %(removal)s; "
                    "please pass the drawstyle separately using the drawstyle "
                    "keyword argument to Line2D or set_drawstyle() method (or "
                    "ds/set_ds()).")
                return ds, ls[len(ds):] or '-'
        return None, ls
