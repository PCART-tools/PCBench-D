    @staticmethod
    def convert_path(gfx_ctx, path, transform):
        wxpath = gfx_ctx.CreatePath()
        for points, code in path.iter_segments(transform):
            if code == Path.MOVETO:
                wxpath.MoveToPoint(*points)
            elif code == Path.LINETO:
                wxpath.AddLineToPoint(*points)
            elif code == Path.CURVE3:
                wxpath.AddQuadCurveToPoint(*points)
            elif code == Path.CURVE4:
                wxpath.AddCurveToPoint(*points)
            elif code == Path.CLOSEPOLY:
                wxpath.CloseSubpath()
        return wxpath
