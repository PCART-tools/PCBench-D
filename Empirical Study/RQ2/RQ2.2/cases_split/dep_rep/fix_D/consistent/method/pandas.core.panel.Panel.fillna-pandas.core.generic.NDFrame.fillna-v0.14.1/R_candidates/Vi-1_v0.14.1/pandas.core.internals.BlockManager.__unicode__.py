    def __unicode__(self):
        output = com.pprint_thing(self.__class__.__name__)
        for i, ax in enumerate(self.axes):
            if i == 0:
                output += u('\nItems: %s') % ax
            else:
                output += u('\nAxis %d: %s') % (i, ax)

        for block in self.blocks:
            output += u('\n%s') % com.pprint_thing(block)
        return output
