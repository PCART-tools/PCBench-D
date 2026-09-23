    @classmethod
    def get_basefile(cls, tex, fontsize, dpi=None):
        """
        Return a filename based on a hash of the string, fontsize, and dpi.
        """
        src = cls._get_tex_source(tex, fontsize) + str(dpi)
        return os.path.join(
            cls.texcache, hashlib.md5(src.encode('utf-8')).hexdigest())
