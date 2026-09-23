class _AnnotationBase:
    def __init__(self,
                 xy,
                 xycoords='data',
                 annotation_clip=None):

        self.xy = xy
        self.xycoords = xycoords
        self.set_annotation_clip(annotation_clip)

        self._draggable = None

    def _get_xy(self, renderer, x, y, s):
        if isinstance(s, tuple):
            s1, s2 = s
        else:
            s1, s2 = s, s
        if s1 == 'data':
            x = float(self.convert_xunits(x))
        if s2 == 'data':
            y = float(self.convert_yunits(y))
        return self._get_xy_transform(renderer, s).transform((x, y))

    def _get_xy_transform(self, renderer, s):

        if isinstance(s, tuple):
            s1, s2 = s
            from matplotlib.transforms import blended_transform_factory
            tr1 = self._get_xy_transform(renderer, s1)
            tr2 = self._get_xy_transform(renderer, s2)
            tr = blended_transform_factory(tr1, tr2)
            return tr
        elif callable(s):
            tr = s(renderer)
            if isinstance(tr, BboxBase):
                return BboxTransformTo(tr)
            elif isinstance(tr, Transform):
                return tr
            else:
                raise RuntimeError("unknown return type ...")
        elif isinstance(s, Artist):
            bbox = s.get_window_extent(renderer)
            return BboxTransformTo(bbox)
        elif isinstance(s, BboxBase):
            return BboxTransformTo(s)
        elif isinstance(s, Transform):
            return s
        elif not isinstance(s, str):
            raise RuntimeError("unknown coordinate type : %s" % s)

        if s == 'data':
            return self.axes.transData
        elif s == 'polar':
            from matplotlib.projections import PolarAxes
            tr = PolarAxes.PolarTransform()
            trans = tr + self.axes.transData
            return trans

        s_ = s.split()
        if len(s_) != 2:
            raise ValueError("%s is not a recognized coordinate" % s)

        bbox0, xy0 = None, None

        bbox_name, unit = s_
        # if unit is offset-like
        if bbox_name == "figure":
            bbox0 = self.figure.figbbox
        elif bbox_name == "subfigure":
            bbox0 = self.figure.bbox
        elif bbox_name == "axes":
            bbox0 = self.axes.bbox
        # elif bbox_name == "bbox":
        #     if bbox is None:
        #         raise RuntimeError("bbox is specified as a coordinate but "
        #                            "never set")
        #     bbox0 = self._get_bbox(renderer, bbox)

        if bbox0 is not None:
            xy0 = bbox0.p0
        elif bbox_name == "offset":
            xy0 = self._get_ref_xy(renderer)

        if xy0 is not None:
            # reference x, y in display coordinate
            ref_x, ref_y = xy0
            if unit == "points":
                # dots per points
                dpp = self.figure.get_dpi() / 72.
                tr = Affine2D().scale(dpp)
            elif unit == "pixels":
                tr = Affine2D()
            elif unit == "fontsize":
                fontsize = self.get_size()
                dpp = fontsize * self.figure.get_dpi() / 72.
                tr = Affine2D().scale(dpp)
            elif unit == "fraction":
                w, h = bbox0.size
                tr = Affine2D().scale(w, h)
            else:
                raise ValueError("%s is not a recognized coordinate" % s)

            return tr.translate(ref_x, ref_y)

        else:
            raise ValueError("%s is not a recognized coordinate" % s)

    def _get_ref_xy(self, renderer):
        """
        Return x, y (in display coordinates) that is to be used for a reference
        of any offset coordinate.
        """
        return self._get_xy(renderer, *self.xy, self.xycoords)

    # def _get_bbox(self, renderer):
    #     if hasattr(bbox, "bounds"):
    #         return bbox
    #     elif hasattr(bbox, "get_window_extent"):
    #         bbox = bbox.get_window_extent()
    #         return bbox
    #     else:
    #         raise ValueError("A bbox instance is expected but got %s" %
    #                          str(bbox))

    def set_annotation_clip(self, b):
        """
        Set the annotation's clipping behavior.

        Parameters
        ----------
        b : bool or None
            - True: the annotation will only be drawn when ``self.xy`` is
              inside the axes.
            - False: the annotation will always be drawn regardless of its
              position.
            - None: the ``self.xy`` will be checked only if *xycoords* is
              "data".
        """
        self._annotation_clip = b

    def get_annotation_clip(self):
        """
        Return the annotation's clipping behavior.

        See `set_annotation_clip` for the meaning of return values.
        """
        return self._annotation_clip

    def _get_position_xy(self, renderer):
        """Return the pixel position of the annotated point."""
        x, y = self.xy
        return self._get_xy(renderer, x, y, self.xycoords)

    def _check_xy(self, renderer):
        """Check whether the annotation at *xy_pixel* should be drawn."""
        b = self.get_annotation_clip()
        if b or (b is None and self.xycoords == "data"):
            # check if self.xy is inside the axes.
            xy_pixel = self._get_position_xy(renderer)
            return self.axes.contains_point(xy_pixel)
        return True

    def draggable(self, state=None, use_blit=False):
        """
        Set whether the annotation is draggable with the mouse.

        Parameters
        ----------
        state : bool or None
            - True or False: set the draggability.
            - None: toggle the draggability.

        Returns
        -------
        DraggableAnnotation or None
            If the annotation is draggable, the corresponding
            `.DraggableAnnotation` helper is returned.
        """
        from matplotlib.offsetbox import DraggableAnnotation
        is_draggable = self._draggable is not None

        # if state is None we'll toggle
        if state is None:
            state = not is_draggable

        if state:
            if self._draggable is None:
                self._draggable = DraggableAnnotation(self, use_blit)
        else:
            if self._draggable is not None:
                self._draggable.disconnect()
            self._draggable = None

        return self._draggable
