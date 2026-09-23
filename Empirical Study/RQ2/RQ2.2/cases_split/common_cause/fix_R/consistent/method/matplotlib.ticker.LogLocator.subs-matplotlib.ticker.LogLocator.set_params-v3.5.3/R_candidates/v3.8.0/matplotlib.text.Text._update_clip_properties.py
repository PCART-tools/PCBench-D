    def _update_clip_properties(self):
        if self._bbox_patch:
            clipprops = dict(clip_box=self.clipbox,
                             clip_path=self._clippath,
                             clip_on=self._clipon)
            self._bbox_patch.update(clipprops)
