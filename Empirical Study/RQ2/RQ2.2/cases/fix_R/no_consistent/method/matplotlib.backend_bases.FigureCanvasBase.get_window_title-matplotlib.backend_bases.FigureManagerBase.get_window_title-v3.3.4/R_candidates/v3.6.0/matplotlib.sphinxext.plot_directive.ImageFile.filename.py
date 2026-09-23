    def filename(self, format):
        return os.path.join(self.dirname, "%s.%s" % (self.basename, format))
