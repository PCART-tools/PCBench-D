    def __repr__(self) -> str:
        output = type(self).__name__
        for i, ax in enumerate(self.axes):
            if i == 0:
                output += f"\nItems: {ax}"
            else:
                output += f"\nAxis {i}: {ax}"

        for block in self.blocks:
            output += f"\n{pprint_thing(block)}"
        return output
