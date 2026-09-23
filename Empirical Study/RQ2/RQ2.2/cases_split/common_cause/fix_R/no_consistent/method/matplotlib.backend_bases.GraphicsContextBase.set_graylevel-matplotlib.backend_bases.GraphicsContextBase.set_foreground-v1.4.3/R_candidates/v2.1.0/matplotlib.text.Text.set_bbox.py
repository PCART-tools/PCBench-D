    def set_bbox(self, rectprops):
        """
        Draw a bounding box around self.  rectprops are any settable
        properties for a FancyBboxPatch, e.g., facecolor='red', alpha=0.5.

          t.set_bbox(dict(facecolor='red', alpha=0.5))

        The default boxstyle is 'square'. The mutation
        scale of the FancyBboxPatch is set to the fontsize.

        ACCEPTS: FancyBboxPatch prop dict
        """

        if rectprops is not None:
            props = rectprops.copy()
            boxstyle = props.pop("boxstyle", None)
            pad = props.pop("pad", None)
            if boxstyle is None:
                boxstyle = "square"
                if pad is None:
                    pad = 4  # points
                pad /= self.get_size()  # to fraction of font size
            else:
                if pad is None:
                    pad = 0.3

            # boxstyle could be a callable or a string
            if (isinstance(boxstyle, six.string_types)
                    and "pad" not in boxstyle):
                boxstyle += ",pad=%0.2f" % pad

            bbox_transmuter = props.pop("bbox_transmuter", None)

            self._bbox_patch = FancyBboxPatch(
                                    (0., 0.),
                                    1., 1.,
                                    boxstyle=boxstyle,
                                    bbox_transmuter=bbox_transmuter,
                                    transform=mtransforms.IdentityTransform(),
                                    **props)
        else:
            self._bbox_patch = None

        self._update_clip_properties()
