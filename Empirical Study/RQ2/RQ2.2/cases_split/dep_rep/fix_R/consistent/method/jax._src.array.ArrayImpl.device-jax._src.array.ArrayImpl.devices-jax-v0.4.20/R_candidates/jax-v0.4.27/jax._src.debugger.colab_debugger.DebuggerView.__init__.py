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
