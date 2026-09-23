    def set_annotation_clip(self, b):
        """
        set *annotation_clip* attribute.

          * True: the annotation will only be drawn when self.xy is inside the
                   axes.
          * False: the annotation will always be drawn regardless of its
                    position.
          * None: the self.xy will be checked only if *xycoords* is "data"
        """
        self._annotation_clip = b
        self.stale = True
