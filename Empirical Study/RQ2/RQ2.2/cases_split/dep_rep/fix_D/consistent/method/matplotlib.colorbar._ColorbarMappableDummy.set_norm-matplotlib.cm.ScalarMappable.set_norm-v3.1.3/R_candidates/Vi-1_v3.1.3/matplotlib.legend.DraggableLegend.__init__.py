    def __init__(self, legend, use_blit=False, update="loc"):
        """
        Wrapper around a `.Legend` to support mouse dragging.

        Parameters
        ----------
        legend : `.Legend`
            The `.Legend` instance to wrap.
        use_blit : bool, optional
            Use blitting for faster image composition. For details see
            :ref:`func-animation`.
        update : {'loc', 'bbox'}, optional
            If "loc", update the *loc* parameter of the legend upon finalizing.
            If "bbox", update the *bbox_to_anchor* parameter.
        """
        self.legend = legend

        if update in ["loc", "bbox"]:
            self._update = update
        else:
            raise ValueError("update parameter '%s' is not supported." %
                             update)

        DraggableOffsetBox.__init__(self, legend, legend._legend_box,
                                    use_blit=use_blit)
