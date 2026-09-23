    @cbook.deprecated("3.3")
    def make_dvi_preview(self, tex, fontsize):
        """
        Generate a dvi file containing latex's layout of tex string.

        It calls make_tex_preview() method and store the size information
        (width, height, descent) in a separate file.

        Return the file name.
        """
        basefile = self.get_basefile(tex, fontsize)
        dvifile = '%s.dvi' % basefile
        baselinefile = '%s.baseline' % basefile

        if not os.path.exists(dvifile) or not os.path.exists(baselinefile):
            texfile = self.make_tex_preview(tex, fontsize)
            report = self._run_checked_subprocess(
                ["latex", "-interaction=nonstopmode", "--halt-on-error",
                 texfile], tex)

            # find the box extent information in the latex output
            # file and store them in ".baseline" file
            m = TexManager._re_vbox.search(report.decode("utf-8"))
            with open(basefile + '.baseline', "w") as fh:
                fh.write(" ".join(m.groups()))

            for fname in glob.glob(basefile + '*'):
                if not fname.endswith(('dvi', 'tex', 'baseline')):
                    try:
                        os.remove(fname)
                    except OSError:
                        pass

        return dvifile
