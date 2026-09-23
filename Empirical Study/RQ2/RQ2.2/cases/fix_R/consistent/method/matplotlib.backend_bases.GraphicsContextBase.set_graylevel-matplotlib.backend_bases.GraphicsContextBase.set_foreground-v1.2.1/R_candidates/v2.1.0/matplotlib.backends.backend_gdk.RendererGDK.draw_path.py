    def draw_path(self, gc, path, transform, rgbFace=None):
        transform = transform + Affine2D(). \
            scale(1.0, -1.0).translate(0, self.height)
        polygons = path.to_polygons(transform, self.width, self.height)
        for polygon in polygons:
            # draw_polygon won't take an arbitrary sequence -- it must be a list
            # of tuples
            polygon = [(int(np.round(x)), int(np.round(y))) for x, y in polygon]
            if rgbFace is not None:
                saveColor = gc.gdkGC.foreground
                gc.gdkGC.foreground = gc.rgb_to_gdk_color(rgbFace)
                self.gdkDrawable.draw_polygon(gc.gdkGC, True, polygon)
                gc.gdkGC.foreground = saveColor
            if gc.gdkGC.line_width > 0:
                self.gdkDrawable.draw_lines(gc.gdkGC, polygon)
