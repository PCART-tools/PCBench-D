    def _get_ifd_dict(
        self, offset: int, group: int | None = None
    ) -> dict[int, Any] | None:
        try:
            # an offset pointer to the location of the nested embedded IFD.
            # It should be a long, but may be corrupted.
            self.fp.seek(offset)
        except (KeyError, TypeError):
            return None
        else:
            from . import TiffImagePlugin

            info = TiffImagePlugin.ImageFileDirectory_v2(self.head, group=group)
            info.load(self.fp)
            return self._fixup_dict(dict(info))
