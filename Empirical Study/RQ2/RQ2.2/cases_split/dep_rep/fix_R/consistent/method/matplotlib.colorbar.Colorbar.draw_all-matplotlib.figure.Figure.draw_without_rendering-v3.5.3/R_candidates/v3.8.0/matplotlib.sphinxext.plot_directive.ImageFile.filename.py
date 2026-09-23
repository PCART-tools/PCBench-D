    def filename(self, format):
        return os.path.join(self.dirname, f"{self.basename}.{format}")
