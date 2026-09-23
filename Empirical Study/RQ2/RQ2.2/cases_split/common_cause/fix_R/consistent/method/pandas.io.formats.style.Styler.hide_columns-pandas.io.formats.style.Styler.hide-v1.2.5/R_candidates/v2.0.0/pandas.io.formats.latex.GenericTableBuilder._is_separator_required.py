    def _is_separator_required(self) -> bool:
        return bool(self.header and self.env_body)
