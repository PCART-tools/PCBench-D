    def named(self) -> dict[str, Any]:
        """
        :returns: dict of name|key: value

        Returns the complete tag dictionary, with named tags where possible.
        """
        return {
            TiffTags.lookup(code, self.group).name: value
            for code, value in self.items()
        }
