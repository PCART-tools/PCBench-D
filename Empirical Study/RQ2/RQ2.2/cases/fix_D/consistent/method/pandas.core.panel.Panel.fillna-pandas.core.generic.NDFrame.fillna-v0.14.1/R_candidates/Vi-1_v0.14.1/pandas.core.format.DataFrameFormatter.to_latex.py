    def to_latex(self, column_format=None, longtable=False):
        """
        Render a DataFrame to a LaTeX tabular/longtable environment output.
        """
        self.escape = self.kwds.get('escape', True)
        #TODO: column_format is not settable in df.to_latex
        def get_col_type(dtype):
            if issubclass(dtype.type, np.number):
                return 'r'
            else:
                return 'l'

        frame = self.frame

        if len(frame.columns) == 0 or len(frame.index) == 0:
            info_line = (u('Empty %s\nColumns: %s\nIndex: %s')
                         % (type(self.frame).__name__,
                            frame.columns, frame.index))
            strcols = [[info_line]]
        else:
            strcols = self._to_str_columns()

        if column_format is None:
            dtypes = self.frame.dtypes.values
            if self.index:
                column_format = 'l%s' % ''.join(map(get_col_type, dtypes))
            else:
                column_format = '%s' % ''.join(map(get_col_type, dtypes))
        elif not isinstance(column_format,
                            compat.string_types):  # pragma: no cover
            raise AssertionError('column_format must be str or unicode, not %s'
                                 % type(column_format))

        def write(buf, frame, column_format, strcols, longtable=False):
            if not longtable:
                buf.write('\\begin{tabular}{%s}\n' % column_format)
                buf.write('\\toprule\n')
            else:
                buf.write('\\begin{longtable}{%s}\n' % column_format)
                buf.write('\\toprule\n')

            nlevels = frame.index.nlevels
            for i, row in enumerate(zip(*strcols)):
                if i == nlevels:
                    buf.write('\\midrule\n')  # End of header
                    if longtable:
                        buf.write('\\endhead\n')
                        buf.write('\\midrule\n')
                        buf.write('\\multicolumn{3}{r}{{Continued on next '
                                  'page}} \\\\\n')
                        buf.write('\midrule\n')
                        buf.write('\endfoot\n\n')
                        buf.write('\\bottomrule\n')
                        buf.write('\\endlastfoot\n')
                if self.escape:
                    crow = [(x.replace('\\', '\\textbackslash') # escape backslashes first
                             .replace('_', '\\_')
                             .replace('%', '\\%')
                             .replace('$', '\\$')
                             .replace('#', '\\#')
                             .replace('{', '\\{')
                             .replace('}', '\\}')
                             .replace('~', '\\textasciitilde')
                             .replace('^', '\\textasciicircum')
                             .replace('&', '\\&') if x else '{}') for x in row]
                else:
                    crow = [x if x else '{}' for x in row]
                buf.write(' & '.join(crow))
                buf.write(' \\\\\n')

            if not longtable:
                buf.write('\\bottomrule\n')
                buf.write('\\end{tabular}\n')
            else:
                buf.write('\\end{longtable}\n')

        if hasattr(self.buf, 'write'):
            write(self.buf, frame, column_format, strcols, longtable)
        elif isinstance(self.buf, compat.string_types):
            with open(self.buf, 'w') as f:
                write(f, frame, column_format, strcols, longtable)
        else:
            raise TypeError('buf is not a file name and it has no write '
                            'method')
