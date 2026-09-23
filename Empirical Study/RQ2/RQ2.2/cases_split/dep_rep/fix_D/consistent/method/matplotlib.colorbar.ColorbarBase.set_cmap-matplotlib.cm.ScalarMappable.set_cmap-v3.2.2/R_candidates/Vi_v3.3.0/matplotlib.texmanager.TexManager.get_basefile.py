    def get_basefile(self, tex, fontsize, dpi=None):
        """
        Return a filename based on a hash of the string, fontsize, and dpi.
        """
        s = ''.join([tex, self.get_font_config(), '%f' % fontsize,
                     self.get_custom_preamble(), str(dpi or '')])
        return os.path.join(
            self.texcache, hashlib.md5(s.encode('utf-8')).hexdigest())
