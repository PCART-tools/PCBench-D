    def draw_gouraud_triangles(self, gc, points, colors, trans):
        assert len(points) == len(colors)
        if len(points) == 0:
            return
        assert points.ndim == 3
        assert points.shape[1] == 3
        assert points.shape[2] == 2
        assert colors.ndim == 3
        assert colors.shape[1] == 3
        assert colors.shape[2] in (1, 4)

        shape = points.shape
        points = points.reshape((shape[0] * shape[1], 2))
        tpoints = trans.transform(points)
        tpoints = tpoints.reshape(shape)
        name, _ = self.file.addGouraudTriangles(tpoints, colors)
        output = self.file.output

        if colors.shape[2] == 1:
            # grayscale
            gc.set_alpha(1.0)
            self.check_gc(gc)
            output(name, Op.shading)
            return

        alpha = colors[0, 0, 3]
        if np.allclose(alpha, colors[:, :, 3]):
            # single alpha value
            gc.set_alpha(alpha)
            self.check_gc(gc)
            output(name, Op.shading)
        else:
            # varying alpha: use a soft mask
            alpha = colors[:, :, 3][:, :, None]
            _, smask_ob = self.file.addGouraudTriangles(tpoints, alpha)
            gstate = self.file._soft_mask_state(smask_ob)
            output(Op.gsave, gstate, Op.setgstate,
                   name, Op.shading,
                   Op.grestore)
