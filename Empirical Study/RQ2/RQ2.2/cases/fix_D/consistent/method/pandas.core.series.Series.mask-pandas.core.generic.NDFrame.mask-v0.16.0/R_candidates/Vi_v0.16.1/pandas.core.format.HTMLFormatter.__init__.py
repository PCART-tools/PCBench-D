    def __init__(self, formatter, classes=None, max_rows=None, max_cols=None):
        self.fmt = formatter
        self.classes = classes

        self.frame = self.fmt.frame
        self.columns = self.fmt.tr_frame.columns
        self.elements = []
        self.bold_rows = self.fmt.kwds.get('bold_rows', False)
        self.escape = self.fmt.kwds.get('escape', True)

        self.max_rows = max_rows or len(self.fmt.frame)
        self.max_cols = max_cols or len(self.fmt.columns)
        self.show_dimensions = self.fmt.show_dimensions
        self.is_truncated = (self.max_rows < len(self.fmt.frame) or
                             self.max_cols < len(self.fmt.columns))
