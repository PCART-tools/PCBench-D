def join(sep: Doc, docs: Sequence[Doc]) -> Doc:
  """Concatenates `docs`, separated by `sep`."""
  docs = list(docs)
  if len(docs) == 0:
    return nil()
  xs = [docs[0]]
  for doc in docs[1:]:
    xs.append(sep)
    xs.append(doc)
  return concat(xs)
