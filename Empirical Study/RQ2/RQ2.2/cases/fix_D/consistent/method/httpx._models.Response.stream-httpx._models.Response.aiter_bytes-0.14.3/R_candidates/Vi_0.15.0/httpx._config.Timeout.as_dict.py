    def as_dict(self) -> typing.Dict[str, typing.Optional[float]]:
        return {
            "connect": self.connect,
            "read": self.read,
            "write": self.write,
            "pool": self.pool,
        }
