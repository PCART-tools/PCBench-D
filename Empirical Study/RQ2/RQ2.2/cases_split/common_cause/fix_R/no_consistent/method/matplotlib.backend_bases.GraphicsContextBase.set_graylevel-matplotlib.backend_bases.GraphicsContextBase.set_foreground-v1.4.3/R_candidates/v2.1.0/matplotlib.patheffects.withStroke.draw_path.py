    def draw_path(self, renderer, gc, tpath, affine, rgbFace):
        Stroke.draw_path(self, renderer, gc, tpath, affine, rgbFace)
        renderer.draw_path(gc, tpath, affine, rgbFace)
