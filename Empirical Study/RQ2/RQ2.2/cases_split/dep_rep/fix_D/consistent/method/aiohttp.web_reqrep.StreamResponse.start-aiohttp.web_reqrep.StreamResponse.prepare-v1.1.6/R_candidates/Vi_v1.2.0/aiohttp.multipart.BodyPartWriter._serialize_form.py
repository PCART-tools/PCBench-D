    def _serialize_form(self, obj):
        if isinstance(obj, Mapping):
            obj = list(obj.items())
        return self._serialize_str(urlencode(obj, doseq=True))
