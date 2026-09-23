    def get_basefile(self, tex, fontsize, dpi=None):
        """
        returns a filename based on a hash of the string, fontsize, and dpi
        """
        s = ''.join([tex, self.get_font_config(), '%f' % fontsize,
                     self.get_custom_preamble(), str(dpi or '')])
        # make sure hash is consistent for all strings, regardless of encoding:
        bytes = six.text_type(s).encode('utf-8')
        return os.path.join(self.texcache, md5(bytes).hexdigest())
