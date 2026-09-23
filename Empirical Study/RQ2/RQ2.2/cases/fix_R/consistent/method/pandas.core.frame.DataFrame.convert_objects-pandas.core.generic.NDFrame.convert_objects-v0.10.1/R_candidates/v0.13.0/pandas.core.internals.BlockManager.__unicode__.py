    def __unicode__(self):
        output = com.pprint_thing(self.__class__.__name__)
        for i, ax in enumerate(self.axes):
            if i == 0:
                output += '\nItems: %s' % ax
            else:
                output += '\nAxis %d: %s' % (i, ax)

        for block in self.blocks:
            output += '\n%s' % com.pprint_thing(block)
        return output
