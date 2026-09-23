    def get_bbox_char(self, c, isord=False):
        if not isord:
            c = ord(c)
        wx, name, bbox = self._metrics[c]
        return bbox
