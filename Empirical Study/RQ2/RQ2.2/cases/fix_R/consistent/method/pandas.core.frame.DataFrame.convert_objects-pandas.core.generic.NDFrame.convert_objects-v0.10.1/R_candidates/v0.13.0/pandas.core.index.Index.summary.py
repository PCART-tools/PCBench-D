    def summary(self, name=None):
        if len(self) > 0:
            head = self[0]
            if hasattr(head, 'format') and\
               not isinstance(head, compat.string_types):
                head = head.format()
            tail = self[-1]
            if hasattr(tail, 'format') and\
               not isinstance(tail, compat.string_types):
                tail = tail.format()
            index_summary = ', %s to %s' % (com.pprint_thing(head),
                                            com.pprint_thing(tail))
        else:
            index_summary = ''

        if name is None:
            name = type(self).__name__
        return '%s: %s entries%s' % (name, len(self), index_summary)
