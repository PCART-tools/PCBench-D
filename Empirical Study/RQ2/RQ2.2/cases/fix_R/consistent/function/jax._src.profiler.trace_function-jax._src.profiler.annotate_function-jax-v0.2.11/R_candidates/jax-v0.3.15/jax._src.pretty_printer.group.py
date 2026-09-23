def group(doc: Doc) -> Doc:
  """Layout alternative groups.

  Prints the group with its breaks as their text (typically spaces) if the
  entire group would fit on the line when printed that way. Otherwise, breaks
  inside the group as printed as newlines.
  """
  return _GroupDoc(doc)
