    def _remap_metadata(self):
        if 'title' in self.metadata:
            self.metadata['name'] = self.metadata['title']
