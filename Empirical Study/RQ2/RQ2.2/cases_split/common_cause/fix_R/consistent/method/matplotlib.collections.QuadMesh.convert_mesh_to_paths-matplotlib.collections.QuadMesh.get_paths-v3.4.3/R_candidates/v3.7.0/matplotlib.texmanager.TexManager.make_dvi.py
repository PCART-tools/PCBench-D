    @classmethod
    def make_dvi(cls, tex, fontsize):
        """
        Generate a dvi file containing latex's layout of tex string.

        Return the file name.
        """
        basefile = cls.get_basefile(tex, fontsize)
        dvifile = '%s.dvi' % basefile
        if not os.path.exists(dvifile):
            texfile = Path(cls.make_tex(tex, fontsize))
            # Generate the dvi in a temporary directory to avoid race
            # conditions e.g. if multiple processes try to process the same tex
            # string at the same time.  Having tmpdir be a subdirectory of the
            # final output dir ensures that they are on the same filesystem,
            # and thus replace() works atomically.  It also allows referring to
            # the texfile with a relative path (for pathological MPLCONFIGDIRs,
            # the absolute path may contain characters (e.g. ~) that TeX does
            # not support; n.b. relative paths cannot traverse parents, or it
            # will be blocked when `openin_any = p` in texmf.cnf).
            cwd = Path(dvifile).parent
            with TemporaryDirectory(dir=cwd) as tmpdir:
                tmppath = Path(tmpdir)
                cls._run_checked_subprocess(
                    ["latex", "-interaction=nonstopmode", "--halt-on-error",
                     f"--output-directory={tmppath.name}",
                     f"{texfile.name}"], tex, cwd=cwd)
                (tmppath / Path(dvifile).name).replace(dvifile)
        return dvifile
