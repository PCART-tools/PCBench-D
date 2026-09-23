    def __init__(self, patch_func=None, **kw):
        """
        Parameters
        ----------
        patch_func : callable, optional
            The function that creates the legend key artist.
            *patch_func* should have the signature::

                def patch_func(legend=legend, orig_handle=orig_handle,
                               xdescent=xdescent, ydescent=ydescent,
                               width=width, height=height, fontsize=fontsize)

            Subsequently the created artist will have its ``update_prop`` method
            called and the appropriate transform will be applied.

        Notes
        -----
        Any other keyword arguments are given to `HandlerBase`.
        """
        HandlerBase.__init__(self, **kw)
        self._patch_func = patch_func
