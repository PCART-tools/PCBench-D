    @property
    def local_name(self) -> str:
        return self.name.replace(_LOCAL_TAG, "")
