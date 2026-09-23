    def _get_footer(self) -> str:
        footer = ""

        if self.length:
            if footer:
                footer += ", "
            footer += f"Length: {len(self.categorical)}"

        level_info = self.categorical._repr_categories_info()

        # Levels are added in a newline
        if footer:
            footer += "\n"
        footer += level_info

        return str(footer)
