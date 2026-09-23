    def write(self, s: Any, indent: int = 0) -> None:
        rs = pprint_thing(s)
        self.elements.append(" " * indent + rs)
