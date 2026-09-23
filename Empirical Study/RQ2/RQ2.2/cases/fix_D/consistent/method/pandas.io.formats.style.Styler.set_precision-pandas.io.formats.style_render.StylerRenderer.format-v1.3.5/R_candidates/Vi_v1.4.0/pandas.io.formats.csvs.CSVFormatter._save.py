    def _save(self) -> None:
        if self._need_to_save_header:
            self._save_header()
        self._save_body()
