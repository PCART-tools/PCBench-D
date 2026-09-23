    def draw_path(self, gc, path, transform, rgbFace=None):
        # docstring inherited
        self.check_gc(gc, rgbFace)
        self.file.writePath(
            path, transform,
            rgbFace is None and gc.get_hatch_path() is None,
            gc.get_sketch_params())
        self.file.output(self.gc.paint())
