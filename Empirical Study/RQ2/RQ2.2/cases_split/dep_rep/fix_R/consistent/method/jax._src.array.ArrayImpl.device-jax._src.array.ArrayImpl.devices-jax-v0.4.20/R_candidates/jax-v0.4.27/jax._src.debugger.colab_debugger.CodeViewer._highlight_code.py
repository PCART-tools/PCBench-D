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
