    def _ensure_entry_points_loaded(self):
        # Load entry points, if they have not already been loaded.
        if not self._loaded_entry_points:
            entries = self._read_entry_points()
            self._validate_and_store_entry_points(entries)
            self._loaded_entry_points = True
