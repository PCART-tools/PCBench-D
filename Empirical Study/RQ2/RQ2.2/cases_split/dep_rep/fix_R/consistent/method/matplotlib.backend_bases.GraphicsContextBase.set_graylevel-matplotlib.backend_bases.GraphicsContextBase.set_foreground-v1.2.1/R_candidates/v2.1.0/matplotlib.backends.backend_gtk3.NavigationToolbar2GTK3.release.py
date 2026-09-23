    def release(self, event):
        try: del self._pixmapBack
        except AttributeError: pass
