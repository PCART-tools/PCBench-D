    def get_prefix_uri(self) -> str:
        from xml.etree.ElementTree import register_namespace

        uri = ""
        if self.namespaces:
            for p, n in self.namespaces.items():
                if isinstance(p, str) and isinstance(n, str):
                    register_namespace(p, n)
            if self.prefix:
                try:
                    uri = f"{{{self.namespaces[self.prefix]}}}"
                except KeyError:
                    raise KeyError(f"{self.prefix} is not included in namespaces")
            else:
                uri = f'{{{self.namespaces[""]}}}'

        return uri
