    def grab_frame(self, **savefig_kwargs):
        if self.embed_frames:
            # Just stop processing if we hit the limit
            if self._hit_limit:
                return
            suffix = '.' + self.frame_format
            f = InMemory()
            self.fig.savefig(f, format=self.frame_format,
                             dpi=self.dpi, **savefig_kwargs)
            imgdata64 = encodebytes(f.getvalue()).decode('ascii')
            self._total_bytes += len(imgdata64)
            if self._total_bytes >= self._bytes_limit:
                warnings.warn("Animation size has reached {0._total_bytes} "
                              "bytes, exceeding the limit of "
                              "{0._bytes_limit}. If you're sure you want "
                              "a larger animation embedded, set the "
                              "animation.embed_limit rc parameter to a "
                              "larger value (in MB). This and further frames"
                              " will be dropped.".format(self))
                self._hit_limit = True
            else:
                self._saved_frames.append(imgdata64)
        else:
            return super(HTMLWriter, self).grab_frame(**savefig_kwargs)
