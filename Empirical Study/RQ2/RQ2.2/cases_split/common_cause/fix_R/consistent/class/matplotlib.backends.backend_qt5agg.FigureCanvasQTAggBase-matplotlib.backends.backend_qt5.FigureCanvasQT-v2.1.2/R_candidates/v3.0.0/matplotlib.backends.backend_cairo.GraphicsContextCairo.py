class GraphicsContextCairo(GraphicsContextBase):
    _joind = {
        'bevel' : cairo.LINE_JOIN_BEVEL,
        'miter' : cairo.LINE_JOIN_MITER,
        'round' : cairo.LINE_JOIN_ROUND,
        }

    _capd = {
        'butt'       : cairo.LINE_CAP_BUTT,
        'projecting' : cairo.LINE_CAP_SQUARE,
        'round'      : cairo.LINE_CAP_ROUND,
        }

    def __init__(self, renderer):
        GraphicsContextBase.__init__(self)
        self.renderer = renderer

    def restore(self):
        self.ctx.restore()

    def set_alpha(self, alpha):
        GraphicsContextBase.set_alpha(self, alpha)
        _alpha = self.get_alpha()
        rgb = self._rgb
        if self.get_forced_alpha():
            self.ctx.set_source_rgba(rgb[0], rgb[1], rgb[2], _alpha)
        else:
            self.ctx.set_source_rgba(rgb[0], rgb[1], rgb[2], rgb[3])

    # def set_antialiased(self, b):
        # cairo has many antialiasing modes, we need to pick one for True and
        # one for False.

    def set_capstyle(self, cs):
        if cs in ('butt', 'round', 'projecting'):
            self._capstyle = cs
            self.ctx.set_line_cap(self._capd[cs])
        else:
            raise ValueError('Unrecognized cap style.  Found %s' % cs)

    def set_clip_rectangle(self, rectangle):
        if not rectangle:
            return
        x, y, w, h = np.round(rectangle.bounds)
        ctx = self.ctx
        ctx.new_path()
        ctx.rectangle(x, self.renderer.height - h - y, w, h)
        ctx.clip()

    def set_clip_path(self, path):
        if not path:
            return
        tpath, affine = path.get_transformed_path_and_affine()
        ctx = self.ctx
        ctx.new_path()
        affine = (affine
                  + Affine2D().scale(1, -1).translate(0, self.renderer.height))
        _append_path(ctx, tpath, affine)
        ctx.clip()

    def set_dashes(self, offset, dashes):
        self._dashes = offset, dashes
        if dashes is None:
            self.ctx.set_dash([], 0)  # switch dashes off
        else:
            self.ctx.set_dash(
                list(self.renderer.points_to_pixels(np.asarray(dashes))),
                offset)

    def set_foreground(self, fg, isRGBA=None):
        GraphicsContextBase.set_foreground(self, fg, isRGBA)
        if len(self._rgb) == 3:
            self.ctx.set_source_rgb(*self._rgb)
        else:
            self.ctx.set_source_rgba(*self._rgb)

    def get_rgb(self):
        return self.ctx.get_source().get_rgba()[:3]

    def set_joinstyle(self, js):
        if js in ('miter', 'round', 'bevel'):
            self._joinstyle = js
            self.ctx.set_line_join(self._joind[js])
        else:
            raise ValueError('Unrecognized join style.  Found %s' % js)

    def set_linewidth(self, w):
        self._linewidth = float(w)
        self.ctx.set_line_width(self.renderer.points_to_pixels(w))
