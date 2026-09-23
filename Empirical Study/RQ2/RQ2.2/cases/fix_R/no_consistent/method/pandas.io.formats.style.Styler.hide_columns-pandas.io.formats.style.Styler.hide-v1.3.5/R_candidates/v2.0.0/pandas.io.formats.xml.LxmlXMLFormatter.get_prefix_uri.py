    def get_prefix_uri(self) -> str:
        uri = ""
        if self.namespaces:
            if self.prefix:
                try:
                    uri = f"{{{self.namespaces[self.prefix]}}}"
                except KeyError:
                    raise KeyError(f"{self.prefix} is not included in namespaces")
            else:
                uri = f'{{{self.namespaces[""]}}}'

        return uri
