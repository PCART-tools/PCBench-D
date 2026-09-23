    def cleanup(self):
        MovieWriter.cleanup(self)

        # Delete temporary files
        if self.clear_temp:
            verbose.report(
                'MovieWriter: clearing temporary fnames=%s' %
                str(self._temp_names),
                level='debug')
            for fname in self._temp_names:
                os.remove(fname)
