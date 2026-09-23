class PolarTransform(mtransforms.Transform):
    """
    The base polar transform.

    This transform maps polar coordinates ``(theta, r)`` into Cartesian
    coordinates ``(x, y) = (r * cos(theta), r * sin(theta))`` (but does not
    handle positioning in screen space).

    Path segments at a fixed radius are automatically transformed to circular
    arcs as long as ``path._interpolation_steps > 1``.
    """

    input_dims = output_dims = 2

    def __init__(self, axis=None, use_rmin=True,
                 _apply_theta_transforms=True):
        super().__init__()
        self._axis = axis
        self._use_rmin = use_rmin
        self._apply_theta_transforms = _apply_theta_transforms

    __str__ = mtransforms._make_str_method(
        "_axis",
        use_rmin="_use_rmin",
        _apply_theta_transforms="_apply_theta_transforms")

    def transform_non_affine(self, tr):
        # docstring inherited
        t, r = np.transpose(tr)
        # PolarAxes does not use the theta transforms here, but apply them for
        # backwards-compatibility if not being used by it.
        if self._apply_theta_transforms and self._axis is not None:
            t *= self._axis.get_theta_direction()
            t += self._axis.get_theta_offset()
        if self._use_rmin and self._axis is not None:
            r = (r - self._axis.get_rorigin()) * self._axis.get_rsign()
        r = np.where(r >= 0, r, np.nan)
        return np.column_stack([r * np.cos(t), r * np.sin(t)])

    def transform_path_non_affine(self, path):
        # docstring inherited
        if not len(path) or path._interpolation_steps == 1:
            return Path(self.transform_non_affine(path.vertices), path.codes)
        xys = []
        codes = []
        last_t = last_r = None
        for trs, c in path.iter_segments():
            trs = trs.reshape((-1, 2))
            if c == Path.LINETO:
                (t, r), = trs
                if t == last_t:  # Same angle: draw a straight line.
                    xys.extend(self.transform_non_affine(trs))
                    codes.append(Path.LINETO)
                elif r == last_r:  # Same radius: draw an arc.
                    # The following is complicated by Path.arc() being
                    # "helpful" and unwrapping the angles, but we don't want
                    # that behavior here.
                    last_td, td = np.rad2deg([last_t, t])
                    if self._use_rmin and self._axis is not None:
                        r = ((r - self._axis.get_rorigin())
                             * self._axis.get_rsign())
                    if last_td <= td:
                        while td - last_td > 360:
                            arc = Path.arc(last_td, last_td + 360)
                            xys.extend(arc.vertices[1:] * r)
                            codes.extend(arc.codes[1:])
                            last_td += 360
                        arc = Path.arc(last_td, td)
                        xys.extend(arc.vertices[1:] * r)
                        codes.extend(arc.codes[1:])
                    else:
                        # The reverse version also relies on the fact that all
                        # codes but the first one are the same.
                        while last_td - td > 360:
                            arc = Path.arc(last_td - 360, last_td)
                            xys.extend(arc.vertices[::-1][1:] * r)
                            codes.extend(arc.codes[1:])
                            last_td -= 360
                        arc = Path.arc(td, last_td)
                        xys.extend(arc.vertices[::-1][1:] * r)
                        codes.extend(arc.codes[1:])
                else:  # Interpolate.
                    trs = cbook.simple_linear_interpolation(
                        np.row_stack([(last_t, last_r), trs]),
                        path._interpolation_steps)[1:]
                    xys.extend(self.transform_non_affine(trs))
                    codes.extend([Path.LINETO] * len(trs))
            else:  # Not a straight line.
                xys.extend(self.transform_non_affine(trs))
                codes.extend([c] * len(trs))
            last_t, last_r = trs[-1]
        return Path(xys, codes)

    def inverted(self):
        # docstring inherited
        return PolarAxes.InvertedPolarTransform(self._axis, self._use_rmin,
                                                self._apply_theta_transforms)
