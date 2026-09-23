    @classmethod
    def make_tex(cls, tex, fontsize):
        """
        Generate a tex file to render the tex string at a specific font size.

        Return the file name.
        """
        texfile = cls.get_basefile(tex, fontsize) + ".tex"
        Path(texfile).write_text(cls._get_tex_source(tex, fontsize),
                                 encoding='utf-8')
        return texfile
