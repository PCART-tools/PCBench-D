    def apply_aspect(self, position=None):
        """
        Adjust the Axes for a specified data aspect ratio.

        Depending on `.get_adjustable` this will modify either the Axes box
        (position) or the view limits. In the former case, `.get_anchor`
        will affect the position.

        Notes
        -----
        This is called automatically when each Axes is drawn.  You may need
        to call it yourself if you need to update the Axes position and/or
        view limits before the Figure is drawn.

        See Also
        --------
        matplotlib.axes.Axes.set_aspect
            for a description of aspect ratio handling.
        matplotlib.axes.Axes.set_adjustable
            defining the parameter to adjust in order to meet the required
            aspect.
        matplotlib.axes.Axes.set_anchor
            defining the position in case of extra space.
        """
        if position is None:
            position = self.get_position(original=True)

        aspect = self.get_aspect()

        if self.name != 'polar':
            xscale, yscale = self.get_xscale(), self.get_yscale()
            if xscale == "linear" and yscale == "linear":
                aspect_scale_mode = "linear"
            elif xscale == "log" and yscale == "log":
                aspect_scale_mode = "log"
            elif ((xscale == "linear" and yscale == "log") or
                  (xscale == "log" and yscale == "linear")):
                if aspect != "auto":
                    warnings.warn(
                        'aspect is not supported for Axes with xscale=%s, '
                        'yscale=%s' % (xscale, yscale), stacklevel=2)
                    aspect = "auto"
            else:  # some custom projections have their own scales.
                pass
        else:
            aspect_scale_mode = "linear"

        if aspect == 'auto':
            self._set_position(position, which='active')
            return

        if aspect == 'equal':
            A = 1
        else:
            A = aspect

        figW, figH = self.get_figure().get_size_inches()
        fig_aspect = figH / figW
        if self._adjustable in ['box', 'box-forced']:
            if self in self._twinned_axes:
                raise RuntimeError("Adjustable 'box' is not allowed in a"
                                   " twinned Axes.  Use 'datalim' instead.")
            if aspect_scale_mode == "log":
                box_aspect = A * self.get_data_ratio_log()
            else:
                box_aspect = A * self.get_data_ratio()
            pb = position.frozen()
            pb1 = pb.shrunk_to_aspect(box_aspect, pb, fig_aspect)
            self._set_position(pb1.anchored(self.get_anchor(), pb), 'active')
            return

        # reset active to original in case it had been changed
        # by prior use of 'box'
        self._set_position(position, which='active')

        xmin, xmax = self.get_xbound()
        ymin, ymax = self.get_ybound()

        if aspect_scale_mode == "log":
            xmin, xmax = math.log10(xmin), math.log10(xmax)
            ymin, ymax = math.log10(ymin), math.log10(ymax)

        xsize = max(abs(xmax - xmin), 1e-30)
        ysize = max(abs(ymax - ymin), 1e-30)

        l, b, w, h = position.bounds
        box_aspect = fig_aspect * (h / w)
        data_ratio = box_aspect / A

        y_expander = (data_ratio * xsize / ysize - 1.0)
        # If y_expander > 0, the dy/dx viewLim ratio needs to increase
        if abs(y_expander) < 0.005:
            return

        if aspect_scale_mode == "log":
            dL = self.dataLim
            dL_width = math.log10(dL.x1) - math.log10(dL.x0)
            dL_height = math.log10(dL.y1) - math.log10(dL.y0)
            xr = 1.05 * dL_width
            yr = 1.05 * dL_height
        else:
            dL = self.dataLim
            xr = 1.05 * dL.width
            yr = 1.05 * dL.height

        xmarg = xsize - xr
        ymarg = ysize - yr
        Ysize = data_ratio * xsize
        Xsize = ysize / data_ratio
        Xmarg = Xsize - xr
        Ymarg = Ysize - yr
        # Setting these targets to, e.g., 0.05*xr does not seem to
        # help.
        xm = 0
        ym = 0

        shared_x = self in self._shared_x_axes
        shared_y = self in self._shared_y_axes
        # Not sure whether we need this check:
        if shared_x and shared_y:
            raise RuntimeError("adjustable='datalim' is not allowed when both"
                               " axes are shared.")

        # If y is shared, then we are only allowed to change x, etc.
        if shared_y:
            adjust_y = False
        else:
            if xmarg > xm and ymarg > ym:
                adjy = ((Ymarg > 0 and y_expander < 0) or
                        (Xmarg < 0 and y_expander > 0))
            else:
                adjy = y_expander > 0
            adjust_y = shared_x or adjy  # (Ymarg > xmarg)

        if adjust_y:
            yc = 0.5 * (ymin + ymax)
            y0 = yc - Ysize / 2.0
            y1 = yc + Ysize / 2.0
            if aspect_scale_mode == "log":
                self.set_ybound((10. ** y0, 10. ** y1))
            else:
                self.set_ybound((y0, y1))
        else:
            xc = 0.5 * (xmin + xmax)
            x0 = xc - Xsize / 2.0
            x1 = xc + Xsize / 2.0
            if aspect_scale_mode == "log":
                self.set_xbound((10. ** x0, 10. ** x1))
            else:
                self.set_xbound((x0, x1))
