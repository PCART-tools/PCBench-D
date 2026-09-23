    @property
    def local_name(self) -> str:
        return self.name.replace(LOCAL_TAG, "")
