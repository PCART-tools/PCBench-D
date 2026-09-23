    def _get_hatch(self, gc, rgbFace):
        """
        Create a new hatch pattern
        """
        if rgbFace is not None:
            rgbFace = tuple(rgbFace)
        edge = gc.get_hatch_color()
        if edge is not None:
            edge = tuple(edge)
        lw = gc.get_hatch_linewidth()
        dictkey = (gc.get_hatch(), rgbFace, edge, lw)
        oid = self._hatchd.get(dictkey)
        if oid is None:
            oid = self._make_id('h', dictkey)
            self._hatchd[dictkey] = ((gc.get_hatch_path(), rgbFace, edge, lw), oid)
        else:
            _, oid = oid
        return oid
