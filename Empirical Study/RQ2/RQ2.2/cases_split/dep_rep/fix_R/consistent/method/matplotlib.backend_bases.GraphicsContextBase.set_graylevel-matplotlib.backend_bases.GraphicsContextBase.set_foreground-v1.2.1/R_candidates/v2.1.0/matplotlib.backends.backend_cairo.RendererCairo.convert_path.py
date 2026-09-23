    @staticmethod
    def convert_path(ctx, path, transform, clip=None):
        for points, code in path.iter_segments(transform, clip=clip):
            if code == Path.MOVETO:
                ctx.move_to(*points)
            elif code == Path.CLOSEPOLY:
                ctx.close_path()
            elif code == Path.LINETO:
                ctx.line_to(*points)
            elif code == Path.CURVE3:
                ctx.curve_to(points[0], points[1],
                             points[0], points[1],
                             points[2], points[3])
            elif code == Path.CURVE4:
                ctx.curve_to(*points)
