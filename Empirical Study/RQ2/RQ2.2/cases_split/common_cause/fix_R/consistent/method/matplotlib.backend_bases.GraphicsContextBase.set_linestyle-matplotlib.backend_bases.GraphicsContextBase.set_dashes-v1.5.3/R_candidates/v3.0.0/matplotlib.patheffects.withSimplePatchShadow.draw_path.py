    def draw_path(self, renderer, gc, tpath, affine, rgbFace):
        SimplePatchShadow.draw_path(self, renderer, gc, tpath, affine, rgbFace)
        renderer.draw_path(gc, tpath, affine, rgbFace)
