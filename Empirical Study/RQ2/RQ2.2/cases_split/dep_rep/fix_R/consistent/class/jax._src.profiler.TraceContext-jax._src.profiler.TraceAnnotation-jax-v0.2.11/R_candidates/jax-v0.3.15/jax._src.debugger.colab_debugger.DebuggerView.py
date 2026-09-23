class DebuggerView(colab_lib.DynamicDOMElement):
  """Main view for the Colab debugger."""

  def __init__(self, frame, *, log_color=""):
    super().__init__()
    self._interaction_log = colab_lib.dynamic(colab_lib.div())
    self._frame_preview = FramePreview(frame)
    self._header = colab_lib.dynamic(
        colab_lib.div(
            colab_lib.span("Breakpoint"),
            style=colab_lib.style({
                "background-color": "var(--colab-secondary-surface-color)",
                "color": "var(--colab-primary-text-color)",
                "padding": "5px 5px 5px 5px",
                "font-weight": "bold",
            })))

  def render(self):
    self._header.render()
    self._frame_preview.render()
    self._interaction_log.render()

  def append(self, child):
    raise NotImplementedError

  def update(self, elem):
    raise NotImplementedError

  def clear(self):
    self._header.clear()
    self._interaction_log.clear()
    self._frame_preview.clear()

  def update_frame(self, frame):
    self._frame_preview.update_frame(frame)

  def log(self, text):
    self._interaction_log.append(colab_lib.pre(text))

  def read(self):
    with output.use_tags(["stdin"]):
      user_input = input()
    output.clear(output_tags=["stdin"])
    return user_input
