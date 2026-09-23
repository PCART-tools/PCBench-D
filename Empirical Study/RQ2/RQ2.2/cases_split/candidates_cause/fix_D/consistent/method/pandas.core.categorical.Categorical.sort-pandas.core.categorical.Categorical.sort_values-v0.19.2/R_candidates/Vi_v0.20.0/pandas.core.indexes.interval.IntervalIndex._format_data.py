    def _format_data(self):

        # TODO: integrate with categorical and make generic
        n = len(self)
        max_seq_items = min((get_option(
            'display.max_seq_items') or n) // 10, 10)

        formatter = str

        if n == 0:
            summary = '[]'
        elif n == 1:
            first = formatter(self[0])
            summary = '[{}]'.format(first)
        elif n == 2:
            first = formatter(self[0])
            last = formatter(self[-1])
            summary = '[{}, {}]'.format(first, last)
        else:

            if n > max_seq_items:
                n = min(max_seq_items // 2, 10)
                head = [formatter(x) for x in self[:n]]
                tail = [formatter(x) for x in self[-n:]]
                summary = '[{} ... {}]'.format(', '.join(head),
                                               ', '.join(tail))
            else:
                head = []
                tail = [formatter(x) for x in self]
                summary = '[{}]'.format(', '.join(tail))

        return summary + self._format_space()
