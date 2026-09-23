    def pop(self, item: Hashable) -> Series | Any:
        result = self[item]
        del self[item]

        return result
