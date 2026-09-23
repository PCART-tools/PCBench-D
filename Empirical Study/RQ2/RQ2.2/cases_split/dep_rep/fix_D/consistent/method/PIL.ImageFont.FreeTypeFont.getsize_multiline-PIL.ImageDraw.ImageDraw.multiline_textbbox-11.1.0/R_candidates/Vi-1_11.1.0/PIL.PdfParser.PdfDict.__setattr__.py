    def __setattr__(self, key: str, value: Any) -> None:
        if key == "data":
            collections.UserDict.__setattr__(self, key, value)
        else:
            self[key.encode("us-ascii")] = value
