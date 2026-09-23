class ToolHome(ViewsPositionsBase):
    """Restore the original view limits."""

    description = 'Reset original view'
    image = 'home'
    default_keymap = mpl.rcParams['keymap.home']
    _on_trigger = 'home'
