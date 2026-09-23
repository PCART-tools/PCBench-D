    def _supports_transparency(self):
        suffix = Path(self.outfile).suffix
        return suffix in {'.apng', '.avif', '.gif', '.webm', '.webp'}
