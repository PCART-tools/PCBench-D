    def __init__(self, legend, use_blit=False, update="loc"):
        """
        update : If "loc", update *loc* parameter of
                 legend upon finalizing. If "bbox", update
                 *bbox_to_anchor* parameter.
        """
        self.legend = legend

        if update in ["loc", "bbox"]:
            self._update = update
        else:
            raise ValueError("update parameter '%s' is not supported." %
                             update)

        DraggableOffsetBox.__init__(self, legend, legend._legend_box,
                                    use_blit=use_blit)
