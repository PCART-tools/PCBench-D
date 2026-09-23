    def _is_palette_needed(self, p):
        for i in range(0, len(p), 3):
            if not (i // 3 == p[i] == p[i + 1] == p[i + 2]):
                return True
        return False
