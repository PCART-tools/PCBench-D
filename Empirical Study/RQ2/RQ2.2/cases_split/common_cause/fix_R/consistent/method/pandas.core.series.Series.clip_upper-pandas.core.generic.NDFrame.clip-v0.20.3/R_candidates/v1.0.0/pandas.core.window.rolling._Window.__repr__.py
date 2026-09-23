    def __repr__(self) -> str:
        """
        Provide a nice str repr of our rolling object.
        """

        attrs_list = (
            f"{attr_name}={getattr(self, attr_name)}"
            for attr_name in self._attributes
            if getattr(self, attr_name, None) is not None
        )
        attrs = ",".join(attrs_list)
        return f"{self._window_type} [{attrs}]"
