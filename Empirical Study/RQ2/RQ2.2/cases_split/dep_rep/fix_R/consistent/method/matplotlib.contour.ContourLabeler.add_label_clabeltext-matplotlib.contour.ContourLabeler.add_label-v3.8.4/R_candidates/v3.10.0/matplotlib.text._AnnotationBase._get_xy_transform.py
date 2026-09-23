    def _get_xy_transform(self, renderer, coords):

        if isinstance(coords, tuple):
            xcoord, ycoord = coords
            from matplotlib.transforms import blended_transform_factory
            tr1 = self._get_xy_transform(renderer, xcoord)
            tr2 = self._get_xy_transform(renderer, ycoord)
            return blended_transform_factory(tr1, tr2)
        elif callable(coords):
            tr = coords(renderer)
            if isinstance(tr, BboxBase):
                return BboxTransformTo(tr)
            elif isinstance(tr, Transform):
                return tr
            else:
                raise TypeError(
                    f"xycoords callable must return a BboxBase or Transform, not a "
                    f"{type(tr).__name__}")
        elif isinstance(coords, Artist):
            bbox = coords.get_window_extent(renderer)
            return BboxTransformTo(bbox)
        elif isinstance(coords, BboxBase):
            return BboxTransformTo(coords)
        elif isinstance(coords, Transform):
            return coords
        elif not isinstance(coords, str):
            raise TypeError(
                f"'xycoords' must be an instance of str, tuple[str, str], Artist, "
                f"Transform, or Callable, not a {type(coords).__name__}")

        if coords == 'data':
            return self.axes.transData
        elif coords == 'polar':
            from matplotlib.projections import PolarAxes
            tr = PolarAxes.PolarTransform(apply_theta_transforms=False)
            trans = tr + self.axes.transData
            return trans

        try:
            bbox_name, unit = coords.split()
        except ValueError:  # i.e. len(coords.split()) != 2.
            raise ValueError(f"{coords!r} is not a valid coordinate") from None

        bbox0, xy0 = None, None

        # if unit is offset-like
        if bbox_name == "figure":
            bbox0 = self.get_figure(root=False).figbbox
        elif bbox_name == "subfigure":
            bbox0 = self.get_figure(root=False).bbox
        elif bbox_name == "axes":
            bbox0 = self.axes.bbox

        # reference x, y in display coordinate
        if bbox0 is not None:
            xy0 = bbox0.p0
        elif bbox_name == "offset":
            xy0 = self._get_position_xy(renderer)
        else:
            raise ValueError(f"{coords!r} is not a valid coordinate")

        if unit == "points":
            tr = Affine2D().scale(
                self.get_figure(root=True).dpi / 72)  # dpi/72 dots per point
        elif unit == "pixels":
            tr = Affine2D()
        elif unit == "fontsize":
            tr = Affine2D().scale(
                self.get_size() * self.get_figure(root=True).dpi / 72)
        elif unit == "fraction":
            tr = Affine2D().scale(*bbox0.size)
        else:
            raise ValueError(f"{unit!r} is not a recognized unit")

        return tr.translate(*xy0)
