    def _format_attrs(self):
        """
        Return a list of tuples of the (attr,formatted_value).
        """
        attrs = super()._format_attrs()
        for attrib in self._attributes:
            if attrib == "freq":
                freq = self.freqstr
                if freq is not None:
                    freq = repr(freq)
                # Argument 1 to "append" of "list" has incompatible type
                # "Tuple[str, Optional[str]]"; expected "Tuple[str, Union[str, int]]"
                attrs.append(("freq", freq))  # type: ignore[arg-type]
        return attrs
