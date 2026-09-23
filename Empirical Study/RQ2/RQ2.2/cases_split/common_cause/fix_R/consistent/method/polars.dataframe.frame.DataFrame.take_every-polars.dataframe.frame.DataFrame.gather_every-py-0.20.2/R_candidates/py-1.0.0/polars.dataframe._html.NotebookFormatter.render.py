    def render(self) -> list[str]:
        """Return the lines needed to render a HTML table."""
        with Tag(self.elements, "div"):
            self.write_style()
            super().render()
        return self.elements
