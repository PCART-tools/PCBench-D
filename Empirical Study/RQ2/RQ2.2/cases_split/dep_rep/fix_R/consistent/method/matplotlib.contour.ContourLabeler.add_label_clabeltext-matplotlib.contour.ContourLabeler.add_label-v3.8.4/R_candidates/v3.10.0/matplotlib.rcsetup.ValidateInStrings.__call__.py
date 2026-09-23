    def __call__(self, s):
        if self._deprecated_since:
            name, = (k for k, v in globals().items() if v is self)
            _api.warn_deprecated(
                self._deprecated_since, name=name, obj_type="function")
        if self.ignorecase and isinstance(s, str):
            s = s.lower()
        if s in self.valid:
            return self.valid[s]
        msg = (f"{s!r} is not a valid value for {self.key}; supported values "
               f"are {[*self.valid.values()]}")
        if (isinstance(s, str)
                and (s.startswith('"') and s.endswith('"')
                     or s.startswith("'") and s.endswith("'"))
                and s[1:-1] in self.valid):
            msg += "; remove quotes surrounding your string"
        raise ValueError(msg)
