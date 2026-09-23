    def get_prefix_uri(self) -> str:
        uri = ""
        if self.namespaces:
            if self.prefix:
                try:
                    uri = f"{{{self.namespaces[self.prefix]}}}"
                except KeyError:
                    raise KeyError(f"{self.prefix} is not included in namespaces")
            elif "" in self.namespaces:
                uri = f'{{{self.namespaces[""]}}}'
            else:
                uri = ""

        return uri
