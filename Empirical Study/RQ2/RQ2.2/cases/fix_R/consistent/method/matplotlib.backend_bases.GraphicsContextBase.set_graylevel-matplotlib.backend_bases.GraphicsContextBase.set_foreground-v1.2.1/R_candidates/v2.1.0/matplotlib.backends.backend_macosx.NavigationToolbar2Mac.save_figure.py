    def save_figure(self, *args):
        filename = _macosx.choose_save_file('Save the figure',
                                            self.canvas.get_default_filename())
        if filename is None: # Cancel
            return
        self.canvas.figure.savefig(filename)
