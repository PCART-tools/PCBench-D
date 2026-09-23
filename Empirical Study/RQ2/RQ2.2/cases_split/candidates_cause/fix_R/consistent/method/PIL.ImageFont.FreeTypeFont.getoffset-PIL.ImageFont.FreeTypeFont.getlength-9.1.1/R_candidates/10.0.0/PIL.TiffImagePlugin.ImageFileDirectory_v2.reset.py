    def reset(self):
        self._tags_v1 = {}  # will remain empty if legacy_api is false
        self._tags_v2 = {}  # main tag storage
        self._tagdata = {}
        self.tagtype = {}  # added 2008-06-05 by Florian Hoech
        self._next = None
        self._offset = None
