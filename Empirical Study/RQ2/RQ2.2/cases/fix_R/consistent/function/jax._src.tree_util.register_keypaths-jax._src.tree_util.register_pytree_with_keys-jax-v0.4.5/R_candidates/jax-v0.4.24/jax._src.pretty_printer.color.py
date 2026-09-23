def color(doc: Doc, *, foreground: Color | None = None,
          background: Color | None = None,
          intensity: Intensity | None = None):
  """ANSI colors.

  Overrides the foreground/background/intensity of the text for the child doc.
  Requires use_colors=True to be set when printing and the `colorama` package
  to be installed; otherwise does nothing.
  """
  return _ColorDoc(doc, foreground=foreground, background=background,
                   intensity=intensity)
