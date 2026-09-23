    def reset(self) -> None:
        self._tags_v1: dict[int, Any] = {}  # will remain empty if legacy_api is false
        self._tags_v2: dict[int, Any] = {}  # main tag storage
        self._tagdata: dict[int, bytes] = {}
        self.tagtype = {}  # added 2008-06-05 by Florian Hoech
        self._next = None
        self._offset: int | None = None
