class SaveFigureBase(ToolBase):
    """Base tool for figure saving."""

    description = 'Save the figure'
    image = 'filesave'
    default_keymap = mpl.rcParams['keymap.save']
