    @classmethod
    def make_png(cls, tex, fontsize, dpi):
        """
        Generate a png file containing latex's rendering of tex string.

        Return the file name.
        """
        basefile = cls.get_basefile(tex, fontsize, dpi)
        pngfile = '%s.png' % basefile
        # see get_rgba for a discussion of the background
        if not os.path.exists(pngfile):
            dvifile = cls.make_dvi(tex, fontsize)
            cmd = ["dvipng", "-bg", "Transparent", "-D", str(dpi),
                   "-T", "tight", "-o", pngfile, dvifile]
            # When testing, disable FreeType rendering for reproducibility; but
            # dvipng 1.16 has a bug (fixed in f3ff241) that breaks --freetype0
            # mode, so for it we keep FreeType enabled; the image will be
            # slightly off.
            if (getattr(mpl, "_called_from_pytest", False) and
                    mpl._get_executable_info("dvipng").raw_version != "1.16"):
                cmd.insert(1, "--freetype0")
            cls._run_checked_subprocess(cmd, tex)
        return pngfile
