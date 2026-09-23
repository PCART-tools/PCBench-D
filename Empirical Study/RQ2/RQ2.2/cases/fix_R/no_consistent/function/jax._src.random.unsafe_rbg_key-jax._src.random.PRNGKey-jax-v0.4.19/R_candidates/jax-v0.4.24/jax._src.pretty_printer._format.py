def _format(doc: Doc, width: int, *, use_color, annotation_prefix) -> str:
  lines = []
  default_colors = _ColorState(Color.RESET, Color.RESET, Intensity.NORMAL)
  annotation_colors = _ColorState(Color.RESET, Color.RESET, Intensity.DIM)
  color_state = default_colors
  agenda = [_State(0, _BreakMode.BREAK, doc, default_colors)]
  k = 0
  line_text = ""
  line_annotations = []
  while len(agenda) > 0:
    i, m, doc, color = agenda.pop()
    if isinstance(doc, _NilDoc):
      pass
    elif isinstance(doc, _TextDoc):
      color_state, color_str = _update_color(use_color, color_state, color)
      line_text += color_str
      line_text += doc.text
      if doc.annotation is not None:
        line_annotations.append(doc.annotation)
      k += len(doc.text)
    elif isinstance(doc, _ConcatDoc):
      agenda.extend(_State(i, m, d, color)
                    for d in reversed(doc.children))
    elif isinstance(doc, _BreakDoc):
      if m == _BreakMode.BREAK:
        if len(line_annotations) > 0:
          color_state, color_str = _update_color(use_color, color_state,
                                                 annotation_colors)
          line_text += color_str
        lines.append(_Line(line_text, k, line_annotations))
        line_text = " " * i
        line_annotations = []
        k = i
      else:
        color_state, color_str = _update_color(use_color, color_state, color)
        line_text += color_str
        line_text += doc.text
        k += len(doc.text)
    elif isinstance(doc, _NestDoc):
      agenda.append(_State(i + doc.n, m, doc.child, color))
    elif isinstance(doc, _GroupDoc):
      # In Lindig's paper, _fits is passed the remainder of the document.
      # I'm pretty sure that's a bug and we care only if the current group fits!
      if (_sparse(doc)
          and _fits(doc, width - k, [(i, _BreakMode.FLAT, doc.child)])):
        agenda.append(_State(i, _BreakMode.FLAT, doc.child, color))
      else:
        agenda.append(_State(i, _BreakMode.BREAK, doc.child, color))
    elif isinstance(doc, _ColorDoc):
      color = _ColorState(doc.foreground or color.foreground,
                          doc.background or color.background,
                          doc.intensity or color.intensity)
      agenda.append(_State(i, m, doc.child, color))
    else:
      raise ValueError("Invalid document ", doc)

  if len(line_annotations) > 0:
    color_state, color_str = _update_color(use_color, color_state,
                                           annotation_colors)
    line_text += color_str
  lines.append(_Line(line_text, k, line_annotations))
  lines = _align_annotations(lines)
  out = "\n".join(
    l.text if l.annotations is None
    else f"{l.text}{annotation_prefix}{l.annotations}" for l in lines)
  color_state, color_str = _update_color(use_color, color_state,
                                         default_colors)
  return out + color_str
