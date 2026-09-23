    def __repr__(self):
        output = pprint_thing(self.__class__.__name__)
        for i, ax in enumerate(self.axes):
            if i == 0:
                output += "\nItems: {ax}".format(ax=ax)
            else:
                output += "\nAxis {i}: {ax}".format(i=i, ax=ax)

        for block in self.blocks:
            output += "\n{block}".format(block=pprint_thing(block))
        return output
