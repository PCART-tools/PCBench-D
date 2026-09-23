    def get(self, key):
        """
        Return the Axes instance that was added with *key*.
        If it is not present, return *None*.
        """
        item = dict(self._elements).get(key)
        if item is None:
            return None
        cbook.warn_deprecated(
            "2.1",
            message="Adding an axes using the same arguments as a previous "
            "axes currently reuses the earlier instance.  In a future "
            "version, a new instance will always be created and returned.  "
            "Meanwhile, this warning can be suppressed, and the future "
            "behavior ensured, by passing a unique label to each axes "
            "instance.")
        return item[1]
