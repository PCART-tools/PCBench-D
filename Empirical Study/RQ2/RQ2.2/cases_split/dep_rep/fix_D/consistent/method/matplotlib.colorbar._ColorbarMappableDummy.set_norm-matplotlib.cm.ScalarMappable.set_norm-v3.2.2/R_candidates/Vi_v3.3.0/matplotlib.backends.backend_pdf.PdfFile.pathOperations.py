    @staticmethod
    def pathOperations(path, transform, clip=None, simplify=None, sketch=None):
        return [Verbatim(_path.convert_to_string(
            path, transform, clip, simplify, sketch,
            6,
            [Op.moveto.op, Op.lineto.op, b'', Op.curveto.op, Op.closepath.op],
            True))]
