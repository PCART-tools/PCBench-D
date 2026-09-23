    def clip_cmd(self, cliprect, clippath):
        """Set clip rectangle. Calls `.pop()` and `.push()`."""
        cmds = []
        # Pop graphics state until we hit the right one or the stack is empty
        while ((self._cliprect, self._clippath) != (cliprect, clippath)
                and self.parent is not None):
            cmds.extend(self.pop())
        # Unless we hit the right one, set the clip polygon
        if ((self._cliprect, self._clippath) != (cliprect, clippath) or
                self.parent is None):
            cmds.extend(self.push())
            if self._cliprect != cliprect:
                cmds.extend([cliprect, Op.rectangle, Op.clip, Op.endpath])
            if self._clippath != clippath:
                path, affine = clippath.get_transformed_path_and_affine()
                cmds.extend(
                    PdfFile.pathOperations(path, affine, simplify=False) +
                    [Op.clip, Op.endpath])
        return cmds
