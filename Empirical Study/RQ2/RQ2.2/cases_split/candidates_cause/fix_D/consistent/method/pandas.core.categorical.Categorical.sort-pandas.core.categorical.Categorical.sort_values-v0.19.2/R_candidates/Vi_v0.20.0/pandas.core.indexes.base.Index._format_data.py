    def _format_data(self):
        """
        Return the formatted data as a unicode string
        """
        from pandas.io.formats.console import get_console_size
        from pandas.io.formats.format import _get_adjustment
        display_width, _ = get_console_size()
        if display_width is None:
            display_width = get_option('display.width') or 80

        space1 = "\n%s" % (' ' * (len(self.__class__.__name__) + 1))
        space2 = "\n%s" % (' ' * (len(self.__class__.__name__) + 2))

        n = len(self)
        sep = ','
        max_seq_items = get_option('display.max_seq_items') or n
        formatter = self._formatter_func

        # do we want to justify (only do so for non-objects)
        is_justify = not (self.inferred_type in ('string', 'unicode') or
                          (self.inferred_type == 'categorical' and
                           is_object_dtype(self.categories)))

        # are we a truncated display
        is_truncated = n > max_seq_items

        # adj can optionaly handle unicode eastern asian width
        adj = _get_adjustment()

        def _extend_line(s, line, value, display_width, next_line_prefix):

            if (adj.len(line.rstrip()) + adj.len(value.rstrip()) >=
                    display_width):
                s += line.rstrip()
                line = next_line_prefix
            line += value
            return s, line

        def best_len(values):
            if values:
                return max([adj.len(x) for x in values])
            else:
                return 0

        if n == 0:
            summary = '[], '
        elif n == 1:
            first = formatter(self[0])
            summary = '[%s], ' % first
        elif n == 2:
            first = formatter(self[0])
            last = formatter(self[-1])
            summary = '[%s, %s], ' % (first, last)
        else:

            if n > max_seq_items:
                n = min(max_seq_items // 2, 10)
                head = [formatter(x) for x in self[:n]]
                tail = [formatter(x) for x in self[-n:]]
            else:
                head = []
                tail = [formatter(x) for x in self]

            # adjust all values to max length if needed
            if is_justify:

                # however, if we are not truncated and we are only a single
                # line, then don't justify
                if (is_truncated or
                        not (len(', '.join(head)) < display_width and
                             len(', '.join(tail)) < display_width)):
                    max_len = max(best_len(head), best_len(tail))
                    head = [x.rjust(max_len) for x in head]
                    tail = [x.rjust(max_len) for x in tail]

            summary = ""
            line = space2

            for i in range(len(head)):
                word = head[i] + sep + ' '
                summary, line = _extend_line(summary, line, word,
                                             display_width, space2)

            if is_truncated:
                # remove trailing space of last line
                summary += line.rstrip() + space2 + '...'
                line = space2

            for i in range(len(tail) - 1):
                word = tail[i] + sep + ' '
                summary, line = _extend_line(summary, line, word,
                                             display_width, space2)

            # last value: no sep added + 1 space of width used for trailing ','
            summary, line = _extend_line(summary, line, tail[-1],
                                         display_width - 2, space2)
            summary += line
            summary += '],'

            if len(summary) > (display_width):
                summary += space1
            else:  # one row
                summary += ' '

            # remove initial space
            summary = '[' + summary[len(space2):]

        return summary
