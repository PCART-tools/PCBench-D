@_api.deprecated("3.6")
class MathtextBackend:
    """
    The base class for the mathtext backend-specific code.  `MathtextBackend`
    subclasses interface between mathtext and specific Matplotlib graphics
    backends.

    Subclasses need to override the following:

    - :meth:`render_glyph`
    - :meth:`render_rect_filled`
    - :meth:`get_results`

    And optionally, if you need to use a FreeType hinting style:

    - :meth:`get_hinting_type`
    """
    def __init__(self):
        self.width = 0
        self.height = 0
        self.depth = 0

    def set_canvas_size(self, w, h, d):
        """Set the dimension of the drawing canvas."""
        self.width  = w
        self.height = h
        self.depth  = d

    def render_glyph(self, ox, oy, info):
        """
        Draw a glyph described by *info* to the reference point (*ox*,
        *oy*).
        """
        raise NotImplementedError()

    def render_rect_filled(self, x1, y1, x2, y2):
        """
        Draw a filled black rectangle from (*x1*, *y1*) to (*x2*, *y2*).
        """
        raise NotImplementedError()

    def get_results(self, box):
        """
        Return a backend-specific tuple to return to the backend after
        all processing is done.
        """
        raise NotImplementedError()

    def get_hinting_type(self):
        """
        Get the FreeType hinting type to use with this particular
        backend.
        """
        return LOAD_NO_HINTING
