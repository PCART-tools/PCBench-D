    @property
    def dimensions_info(self) -> str:
        return f"\n\n[{len(self.frame)} rows x {len(self.frame.columns)} columns]"
