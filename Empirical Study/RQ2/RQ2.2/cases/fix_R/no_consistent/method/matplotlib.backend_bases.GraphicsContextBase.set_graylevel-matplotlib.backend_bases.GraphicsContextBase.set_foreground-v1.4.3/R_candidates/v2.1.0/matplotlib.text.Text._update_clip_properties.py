    def _update_clip_properties(self):
        clipprops = dict(clip_box=self.clipbox,
                         clip_path=self._clippath,
                         clip_on=self._clipon)

        if self._bbox_patch:
            bbox = self._bbox_patch.update(clipprops)
