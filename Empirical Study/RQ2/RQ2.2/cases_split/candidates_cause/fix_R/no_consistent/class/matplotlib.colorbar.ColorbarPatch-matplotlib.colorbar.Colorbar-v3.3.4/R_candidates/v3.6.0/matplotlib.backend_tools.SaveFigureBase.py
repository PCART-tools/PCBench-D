class SaveFigureBase(ToolBase):
    """Base tool for figure saving."""

    description = 'Save the figure'
    image = 'filesave'
    default_keymap = property(lambda self: mpl.rcParams['keymap.save'])
