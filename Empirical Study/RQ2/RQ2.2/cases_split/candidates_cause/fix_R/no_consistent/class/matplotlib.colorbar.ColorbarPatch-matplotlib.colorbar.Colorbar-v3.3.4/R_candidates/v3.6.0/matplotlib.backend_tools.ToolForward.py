class ToolForward(ViewsPositionsBase):
    """Move forward in the view lim stack."""

    description = 'Forward to next view'
    image = 'forward'
    default_keymap = property(lambda self: mpl.rcParams['keymap.forward'])
    _on_trigger = 'forward'
