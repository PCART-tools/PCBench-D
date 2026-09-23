class ToolBack(ViewsPositionsBase):
    """Move back up the view limits stack."""

    description = 'Back to previous view'
    image = 'back'
    default_keymap = property(lambda self: mpl.rcParams['keymap.back'])
    _on_trigger = 'back'
