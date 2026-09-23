    def _set(self, profile: core.CmsProfile, filename: str | None = None) -> None:
        self.profile = profile
        self.filename = filename
        self.product_name = None  # profile.product_name
        self.product_info = None  # profile.product_info
