    def atomize(self, declarations):
        for prop, value in declarations:
            attr = "expand_" + prop.replace("-", "_")
            try:
                expand = getattr(self, attr)
            except AttributeError:
                yield prop, value
            else:
                for prop, value in expand(prop, value):
                    yield prop, value
