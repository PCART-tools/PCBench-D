    @artist.allow_rasterization
    def draw(self, renderer):
        """
        Draws the `.Text` object to the given *renderer*.
        """
        if renderer is not None:
            self._renderer = renderer
        if not self.get_visible():
            return
        if self.get_text() == '':
            return

        renderer.open_group('text', self.get_gid())

        with _wrap_text(self) as textobj:
            bbox, info, descent = textobj._get_layout(renderer)
            trans = textobj.get_transform()

            # don't use textobj.get_position here, which refers to text
            # position in Text, and dash position in TextWithDash:
            posx = float(textobj.convert_xunits(textobj._x))
            posy = float(textobj.convert_yunits(textobj._y))
            posx, posy = trans.transform((posx, posy))
            if not np.isfinite(posx) or not np.isfinite(posy):
                _log.warning("posx and posy should be finite values")
                return
            canvasw, canvash = renderer.get_canvas_width_height()

            # draw the FancyBboxPatch
            if textobj._bbox_patch:
                textobj._draw_bbox(renderer, posx, posy)

            gc = renderer.new_gc()
            gc.set_foreground(textobj.get_color())
            gc.set_alpha(textobj.get_alpha())
            gc.set_url(textobj._url)
            textobj._set_gc_clip(gc)

            angle = textobj.get_rotation()

            for line, wh, x, y in info:

                mtext = textobj if len(info) == 1 else None
                x = x + posx
                y = y + posy
                if renderer.flipy():
                    y = canvash - y
                clean_line, ismath = textobj._preprocess_math(line)

                if textobj.get_path_effects():
                    from matplotlib.patheffects import PathEffectRenderer
                    textrenderer = PathEffectRenderer(
                                        textobj.get_path_effects(), renderer)
                else:
                    textrenderer = renderer

                if textobj.get_usetex():
                    textrenderer.draw_tex(gc, x, y, clean_line,
                                          textobj._fontproperties, angle,
                                          mtext=mtext)
                else:
                    textrenderer.draw_text(gc, x, y, clean_line,
                                           textobj._fontproperties, angle,
                                           ismath=ismath, mtext=mtext)

        gc.restore()
        renderer.close_group('text')
        self.stale = False
