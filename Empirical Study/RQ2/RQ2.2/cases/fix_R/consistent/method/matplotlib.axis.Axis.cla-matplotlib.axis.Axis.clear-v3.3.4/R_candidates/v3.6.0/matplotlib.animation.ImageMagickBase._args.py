    def _args(self):
        # ImageMagick does not recognize "raw".
        fmt = "rgba" if self.frame_format == "raw" else self.frame_format
        extra_args = (self.extra_args if self.extra_args is not None
                      else mpl.rcParams[self._args_key])
        return [
            self.bin_path(),
            "-size", "%ix%i" % self.frame_size,
            "-depth", "8",
            "-delay", str(100 / self.fps),
            "-loop", "0",
            f"{fmt}:{self.input_names}",
            *extra_args,
            self.outfile,
        ]
