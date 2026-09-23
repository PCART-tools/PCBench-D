    def _str_fullmatch(
        self, pat, case: bool = True, flags: int = 0, na: Scalar | None = None
    ):
        if not pat.endswith("$") or pat.endswith("//$"):
            pat = f"{pat}$"
        return self._str_match(pat, case, flags, na)
