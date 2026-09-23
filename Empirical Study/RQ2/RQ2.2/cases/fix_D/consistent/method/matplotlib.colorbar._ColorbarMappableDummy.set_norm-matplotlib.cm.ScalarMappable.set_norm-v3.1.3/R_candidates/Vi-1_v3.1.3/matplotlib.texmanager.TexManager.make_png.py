    def make_png(self, tex, fontsize, dpi):
        """
        Generate a png file containing latex's rendering of tex string.

        Return the file name.
        """
        basefile = self.get_basefile(tex, fontsize, dpi)
        pngfile = '%s.png' % basefile
        # see get_rgba for a discussion of the background
        if not os.path.exists(pngfile):
            dvifile = self.make_dvi(tex, fontsize)
            self._run_checked_subprocess(
                ["dvipng", "-bg", "Transparent", "-D", str(dpi),
                 "-T", "tight", "-o", pngfile, dvifile], tex)
        return pngfile
