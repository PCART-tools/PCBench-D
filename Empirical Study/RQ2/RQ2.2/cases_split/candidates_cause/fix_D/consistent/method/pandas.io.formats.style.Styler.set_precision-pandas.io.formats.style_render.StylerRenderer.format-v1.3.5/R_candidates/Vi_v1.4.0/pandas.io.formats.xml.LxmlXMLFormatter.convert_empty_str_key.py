    def convert_empty_str_key(self) -> None:
        """
        Replace zero-lengh string in `namespaces`.

        This method will replce '' with None to align to `lxml`
        requirement that empty string prefixes are not allowed.
        """

        if self.namespaces and "" in self.namespaces.keys():
            self.namespaces[None] = self.namespaces.pop("", "default")
