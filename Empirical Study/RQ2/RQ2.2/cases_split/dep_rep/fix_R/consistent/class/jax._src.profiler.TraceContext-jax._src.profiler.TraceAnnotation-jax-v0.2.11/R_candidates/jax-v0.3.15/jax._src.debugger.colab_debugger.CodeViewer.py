class CodeViewer(colab_lib.DynamicDOMElement):
  """A mutable DOM element that displays code as HTML."""

  def __init__(self, code_: str, highlights: List[int], linenostart: int = 1):
    self._code = code_
    self._highlights = highlights
    self._view = colab_lib.dynamic(colab_lib.div())
    self._linenostart = linenostart

  def render(self):
    self.update_code(
        self._code, self._highlights, linenostart=self._linenostart)

  def clear(self):
    self._view.clear()

  def append(self, child):
    raise NotImplementedError

  def update(self, elem):
    self._view.update(elem)

  def _highlight_code(self, code: str, highlights, linenostart: int):
    is_dark_mode = output.eval_js(
        'document.documentElement.matches("[theme=dark]");')
    code_style = "monokai" if is_dark_mode else "default"
    hl_color = "#4e56b7" if is_dark_mode else "#fff7c1"
    if IS_PYGMENTS_ENABLED:
      lexer = pygments.lexers.get_lexer_by_name("python")
      formatter = pygments.formatters.HtmlFormatter(
          full=False,
          hl_lines=highlights,
          linenos=True,
          linenostart=linenostart,
          style=code_style)
      if hl_color:
        formatter.style.highlight_color = hl_color
      css_ = formatter.get_style_defs()
      code = pygments.highlight(code, lexer, formatter)
    else:
      return "";
    return code, css_

  def update_code(self, code_, highlights, *, linenostart: int = 1):
    """Updates the code viewer to use new code."""
    self._code = code_
    self._view.clear()
    code_, css_ = self._highlight_code(self._code, highlights, linenostart)
    uuid_ = uuid.uuid4()
    code_div = colab_lib.div(
        colab_lib.css(css_),
        code_,
        id=f"code-{uuid_}",
        style=colab_lib.style({
            "max-height": "500px",
            "overflow-y": "scroll",
            "background-color": "var(--colab-border-color)",
            "padding": "5px 5px 5px 5px",
        }))
    if highlights:
      percent_scroll = highlights[0] / len(self._code.split("\n"))
    else:
      percent_scroll = 0.
    self.update(code_div)
    # Scroll to where the line is
    output.eval_js("""
    console.log("{id}")
    var elem = document.getElementById("{id}")
    var maxScrollPosition = elem.scrollHeight - elem.clientHeight;
    elem.scrollTop = maxScrollPosition * {percent_scroll}
    """.format(id=f"code-{uuid_}", percent_scroll=percent_scroll))
