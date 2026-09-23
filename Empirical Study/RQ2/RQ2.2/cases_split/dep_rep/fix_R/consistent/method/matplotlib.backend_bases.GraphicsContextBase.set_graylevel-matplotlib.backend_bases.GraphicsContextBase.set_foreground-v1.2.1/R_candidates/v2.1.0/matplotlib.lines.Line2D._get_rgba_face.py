    def _get_rgba_face(self, alt=False):
        facecolor = self._get_markerfacecolor(alt=alt)
        if (isinstance(facecolor, six.string_types)
                and facecolor.lower() == 'none'):
            rgbaFace = None
        else:
            rgbaFace = mcolors.to_rgba(facecolor, self._alpha)
        return rgbaFace
