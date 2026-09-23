    def atomize(self, declarations: Iterable) -> Generator[tuple[str, str], None, None]:
        for prop, value in declarations:
            prop = prop.lower()
            value = value.lower()
            if prop in self.CSS_EXPANSIONS:
                expand = self.CSS_EXPANSIONS[prop]
                yield from expand(self, prop, value)
            else:
                yield prop, value
