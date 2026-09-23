    @staticmethod
    @cbook.deprecated("3.0")
    def convert_path(ctx, path, transform, clip=None):
        _append_path(ctx, path, transform, clip)
