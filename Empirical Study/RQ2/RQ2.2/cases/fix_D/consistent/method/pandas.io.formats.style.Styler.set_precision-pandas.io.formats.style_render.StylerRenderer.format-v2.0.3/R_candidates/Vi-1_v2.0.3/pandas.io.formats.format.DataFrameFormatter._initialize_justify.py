    def _initialize_justify(self, justify: str | None) -> str:
        if justify is None:
            return get_option("display.colheader_justify")
        else:
            return justify
