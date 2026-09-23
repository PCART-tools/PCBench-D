    def _convert_path(self, path, transform=None, clip=None, simplify=None,
                      sketch=None):
        if clip:
            clip = (0.0, 0.0, self.width, self.height)
        else:
            clip = None
        return _path.convert_to_string(
            path, transform, clip, simplify, sketch, 6,
            [b'M', b'L', b'Q', b'C', b'z'], False).decode('ascii')
