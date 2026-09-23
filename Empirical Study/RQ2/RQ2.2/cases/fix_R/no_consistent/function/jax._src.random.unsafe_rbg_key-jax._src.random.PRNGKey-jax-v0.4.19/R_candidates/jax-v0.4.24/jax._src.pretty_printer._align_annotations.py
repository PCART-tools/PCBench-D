def _align_annotations(lines):
  # TODO: Hafiz also implements a local alignment mode, where groups of lines
  # with annotations are aligned together.
  maxlen = max(l.width for l in lines)
  out = []
  for l in lines:
    if len(l.annotations) == 0:
      out.append(l._replace(annotations=None))
    elif len(l.annotations) == 1:
      out.append(l._replace(text=l.text + " " * (maxlen - l.width),
                            annotations=l.annotations[0]))
    else:
      out.append(l._replace(text=l.text + " " * (maxlen - l.width),
                            annotations=l.annotations[0]))
      for a in l.annotations[1:]:
        out.append(_Line(text=" " * maxlen, width=l.width, annotations=a))
  return out
