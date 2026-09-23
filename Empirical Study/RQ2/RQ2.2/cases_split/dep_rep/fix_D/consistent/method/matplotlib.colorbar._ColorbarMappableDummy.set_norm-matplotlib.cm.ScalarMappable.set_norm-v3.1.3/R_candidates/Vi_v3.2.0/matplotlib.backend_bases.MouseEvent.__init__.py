    def __init__(self, name, canvas, x, y, button=None, key=None,
                 step=0, dblclick=False, guiEvent=None):
        """
        (*x*, *y*) in figure coords ((0, 0) = bottom left)
        button pressed None, 1, 2, 3, 'up', 'down'
        """
        LocationEvent.__init__(self, name, canvas, x, y, guiEvent=guiEvent)
        if button in MouseButton.__members__.values():
            button = MouseButton(button)
        self.button = button
        self.key = key
        self.step = step
        self.dblclick = dblclick
