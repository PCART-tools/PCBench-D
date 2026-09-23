    def make_dvi(self, tex, fontsize):
        """
        Generate a dvi file containing latex's layout of tex string.

        Return the file name.
        """

        if rcParams['text.latex.preview']:
            return self.make_dvi_preview(tex, fontsize)

        basefile = self.get_basefile(tex, fontsize)
        dvifile = '%s.dvi' % basefile
        if not os.path.exists(dvifile):
            texfile = self.make_tex(tex, fontsize)
            with cbook._lock_path(texfile):
                self._run_checked_subprocess(
                    ["latex", "-interaction=nonstopmode", "--halt-on-error",
                     texfile], tex)
            for fname in glob.glob(basefile + '*'):
                if not fname.endswith(('dvi', 'tex')):
                    try:
                        os.remove(fname)
                    except OSError:
                        pass

        return dvifile
