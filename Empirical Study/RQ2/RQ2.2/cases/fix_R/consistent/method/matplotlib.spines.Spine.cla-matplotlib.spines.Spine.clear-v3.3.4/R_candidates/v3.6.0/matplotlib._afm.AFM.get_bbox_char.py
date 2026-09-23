    def get_bbox_char(self, c, isord=False):
        if not isord:
            c = ord(c)
        return self._metrics[c].bbox
