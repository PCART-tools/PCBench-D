    def __init__(self, canvas):
        self.canvas = canvas  # Needed by the _macosx __init__.
        data_path = cbook._get_data_path('images')
        _, tooltips, image_names, _ = zip(*NavigationToolbar2.toolitems)
        _macosx.NavigationToolbar2.__init__(
            self,
            tuple(str(data_path / image_name) + ".pdf"
                  for image_name in image_names if image_name is not None),
            tuple(tooltip for tooltip in tooltips if tooltip is not None))
        NavigationToolbar2.__init__(self, canvas)
