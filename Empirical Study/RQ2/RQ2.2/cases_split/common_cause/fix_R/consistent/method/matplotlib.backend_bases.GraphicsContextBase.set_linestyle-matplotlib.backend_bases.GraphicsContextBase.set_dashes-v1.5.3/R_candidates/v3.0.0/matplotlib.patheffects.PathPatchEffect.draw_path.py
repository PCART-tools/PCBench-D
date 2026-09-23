    def draw_path(self, renderer, gc, tpath, affine, rgbFace):
        affine = self._offset_transform(renderer, affine)
        self.patch._path = tpath
        self.patch.set_transform(affine)
        self.patch.set_clip_box(gc.get_clip_rectangle())
        clip_path = gc.get_clip_path()
        if clip_path:
            self.patch.set_clip_path(*clip_path)
        self.patch.draw(renderer)
