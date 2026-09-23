    def _maybe_update_attributes(self, attrs):
        """ Update Index attributes (e.g. freq) depending on op """
        freq = attrs.get("freq", None)
        if freq is not None:
            # no need to infer if freq is None
            attrs["freq"] = "infer"
        return attrs
