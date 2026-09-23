def _update_color(use_color: bool, state: _ColorState, update: _ColorState
                 ) -> tuple[_ColorState, str]:
  if not use_color or colorama is None:
    return update, ""
  color_str = ""
  if state.foreground != update.foreground:
    color_str += getattr(colorama.Fore, str(update.foreground.name))
  if state.background != update.background:
    color_str += getattr(colorama.Back, str(update.background.name))
  if state.intensity != update.intensity:
    color_str += colorama.Style.NORMAL  # pytype: disable=unsupported-operands
    color_str += getattr(colorama.Style, str(update.intensity.name))
  return update, color_str
