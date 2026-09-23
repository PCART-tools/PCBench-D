@docstring.Substitution(_RECTANGLESELECTOR_PARAMETERS_DOCSTRING.replace(
    '__ARTIST_NAME__', 'ellipse'))
class EllipseSelector(RectangleSelector):
    """
    Select an elliptical region of an axes.

    For the cursor to remain responsive you must keep a reference to it.

    Press and release events triggered at the same coordinates outside the
    selection will clear the selector, except when
    ``ignore_event_outside=True``.

    %s

    Examples
    --------
    :doc:`/gallery/widgets/rectangle_selector`
    """

    _shape_klass = Ellipse
    draw_shape = _api.deprecate_privatize_attribute('3.5')

    def _draw_shape(self, extents):
        x0, x1, y0, y1 = extents
        xmin, xmax = sorted([x0, x1])
        ymin, ymax = sorted([y0, y1])
        center = [x0 + (x1 - x0) / 2., y0 + (y1 - y0) / 2.]
        a = (xmax - xmin) / 2.
        b = (ymax - ymin) / 2.

        if self._drawtype == 'box':
            self._selection_artist.center = center
            self._selection_artist.width = 2 * a
            self._selection_artist.height = 2 * b
        else:
            rad = np.deg2rad(np.arange(31) * 12)
            x = a * np.cos(rad) + center[0]
            y = b * np.sin(rad) + center[1]
            self._selection_artist.set_data(x, y)

    @property
    def _rect_bbox(self):
        if self._drawtype == 'box':
            x, y = self._selection_artist.center
            width = self._selection_artist.width
            height = self._selection_artist.height
            return x - width / 2., y - height / 2., width, height
        else:
            x, y = self._selection_artist.get_data()
            x0, x1 = min(x), max(x)
            y0, y1 = min(y), max(y)
            return x0, y0, x1 - x0, y1 - y0
