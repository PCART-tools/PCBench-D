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
