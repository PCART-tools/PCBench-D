    def __init__(self, patch_func=None, **kw):
        """
        The HandlerPatch class optionally takes a function ``patch_func``
        who's responsibility is to create the legend key artist. The
        ``patch_func`` should have the signature::

            def patch_func(legend=legend, orig_handle=orig_handle,
                           xdescent=xdescent, ydescent=ydescent,
                           width=width, height=height, fontsize=fontsize)

        Subsequently the created artist will have its ``update_prop`` method
        called and the appropriate transform will be applied.

        """
        HandlerBase.__init__(self, **kw)
        self._patch_func = patch_func
