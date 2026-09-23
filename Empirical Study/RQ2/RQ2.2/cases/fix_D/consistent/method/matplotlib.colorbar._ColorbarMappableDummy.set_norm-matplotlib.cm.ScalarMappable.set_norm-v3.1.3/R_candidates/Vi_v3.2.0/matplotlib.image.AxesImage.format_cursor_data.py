    def format_cursor_data(self, data):
        if np.ndim(data) == 0 and self.colorbar:
            return (
                "["
                + cbook.strip_math(
                    self.colorbar.formatter.format_data_short(data)).strip()
                + "]")
        else:
            return super().format_cursor_data(data)
