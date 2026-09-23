    def make_dvi(self, tex, fontsize):
        """
        Generate a dvi file containing latex's layout of tex string.

        Return the file name.
        """

        if dict.__getitem__(rcParams, 'text.latex.preview'):
            return self.make_dvi_preview(tex, fontsize)

        basefile = self.get_basefile(tex, fontsize)
        dvifile = '%s.dvi' % basefile
        if not os.path.exists(dvifile):
            texfile = self.make_tex(tex, fontsize)
            # Generate the dvi in a temporary directory to avoid race
            # conditions e.g. if multiple processes try to process the same tex
            # string at the same time.  Having tmpdir be a subdirectory of the
            # final output dir ensures that they are on the same filesystem,
            # and thus replace() works atomically.
            with TemporaryDirectory(dir=Path(dvifile).parent) as tmpdir:
                self._run_checked_subprocess(
                    ["latex", "-interaction=nonstopmode", "--halt-on-error",
                     texfile], tex, cwd=tmpdir)
                (Path(tmpdir) / Path(dvifile).name).replace(dvifile)
        return dvifile
