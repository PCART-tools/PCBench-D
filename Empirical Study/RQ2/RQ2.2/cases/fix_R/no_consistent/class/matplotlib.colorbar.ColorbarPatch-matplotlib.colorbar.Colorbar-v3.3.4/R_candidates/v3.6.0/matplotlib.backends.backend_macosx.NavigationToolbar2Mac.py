class NavigationToolbar2Mac(_macosx.NavigationToolbar2, NavigationToolbar2):

    def __init__(self, canvas):
        data_path = cbook._get_data_path('images')
        _, tooltips, image_names, _ = zip(*NavigationToolbar2.toolitems)
        _macosx.NavigationToolbar2.__init__(
            self, canvas,
            tuple(str(data_path / image_name) + ".pdf"
                  for image_name in image_names if image_name is not None),
            tuple(tooltip for tooltip in tooltips if tooltip is not None))
        NavigationToolbar2.__init__(self, canvas)

    def draw_rubberband(self, event, x0, y0, x1, y1):
        self.canvas.set_rubberband(int(x0), int(y0), int(x1), int(y1))

    def remove_rubberband(self):
        self.canvas.remove_rubberband()

    def save_figure(self, *args):
        directory = os.path.expanduser(mpl.rcParams['savefig.directory'])
        filename = _macosx.choose_save_file('Save the figure',
                                            directory,
                                            self.canvas.get_default_filename())
        if filename is None:  # Cancel
            return
        # Save dir for next time, unless empty str (which means use cwd).
        if mpl.rcParams['savefig.directory']:
            mpl.rcParams['savefig.directory'] = os.path.dirname(filename)
        self.canvas.figure.savefig(filename)

    @_api.deprecated("3.6", alternative='configure_subplots()')
    def prepare_configure_subplots(self):
        toolfig = Figure(figsize=(6, 3))
        canvas = FigureCanvasMac(toolfig)
        toolfig.subplots_adjust(top=0.9)
        # Need to keep a reference to the tool.
        _tool = SubplotTool(self.canvas.figure, toolfig)
        return canvas
