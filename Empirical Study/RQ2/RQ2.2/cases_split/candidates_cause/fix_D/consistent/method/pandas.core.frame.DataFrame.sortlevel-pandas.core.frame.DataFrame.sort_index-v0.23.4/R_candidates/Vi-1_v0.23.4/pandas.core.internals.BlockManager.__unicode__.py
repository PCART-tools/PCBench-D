    def __unicode__(self):
        output = pprint_thing(self.__class__.__name__)
        for i, ax in enumerate(self.axes):
            if i == 0:
                output += u('\nItems: {ax}'.format(ax=ax))
            else:
                output += u('\nAxis {i}: {ax}'.format(i=i, ax=ax))

        for block in self.blocks:
            output += u('\n{block}'.format(block=pprint_thing(block)))
        return output
