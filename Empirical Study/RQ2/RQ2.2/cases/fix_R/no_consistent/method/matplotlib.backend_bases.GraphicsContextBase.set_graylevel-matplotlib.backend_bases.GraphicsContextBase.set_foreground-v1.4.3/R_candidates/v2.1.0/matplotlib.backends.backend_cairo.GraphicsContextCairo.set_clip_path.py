    def set_clip_path(self, path):
        if not path:
            return
        tpath, affine = path.get_transformed_path_and_affine()
        ctx = self.ctx
        ctx.new_path()
        affine = (affine
                  + Affine2D().scale(1, -1).translate(0, self.renderer.height))
        RendererCairo.convert_path(ctx, tpath, affine)
        ctx.clip()
