    def write_result(self, buf):
        indent = 0
        frame = self.frame

        _classes = ['dataframe']  # Default class.
        if self.classes is not None:
            if isinstance(self.classes, str):
                self.classes = self.classes.split()
            if not isinstance(self.classes, (list, tuple)):
                raise AssertionError(('classes must be list or tuple, '
                                      'not %s') % type(self.classes))
            _classes.extend(self.classes)

        self.write('<table border="1" class="%s">' % ' '.join(_classes),
                   indent)

        if len(frame.columns) == 0 or len(frame.index) == 0:
            self.write('<tbody>', indent + self.indent_delta)
            self.write_tr([repr(frame.index),
                           'Empty %s' % type(frame).__name__],
                          indent + (2 * self.indent_delta),
                          self.indent_delta)
            self.write('</tbody>', indent + self.indent_delta)
        else:
            indent += self.indent_delta
            indent = self._write_header(indent)
            indent = self._write_body(indent)

        self.write('</table>', indent)
        if self.fmt.show_dimensions:
            by = chr(215) if compat.PY3 else unichr(215)  # ×
            self.write(u('<p>%d rows %s %d columns</p>') %
                       (len(frame), by, len(frame.columns)))
        _put_lines(buf, self.elements)
