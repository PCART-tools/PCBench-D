    @mpl.cbook.deprecated("2.2")
    def make_ps(self, tex, fontsize):
        """
        Generate a postscript file containing latex's rendering of tex string.

        Return the file name.
        """
        basefile = self.get_basefile(tex, fontsize)
        psfile = '%s.epsf' % basefile
        if not os.path.exists(psfile):
            dvifile = self.make_dvi(tex, fontsize)
            self._run_checked_subprocess(
                ["dvips", "-q", "-E", "-o", psfile, dvifile], tex)
        return psfile
