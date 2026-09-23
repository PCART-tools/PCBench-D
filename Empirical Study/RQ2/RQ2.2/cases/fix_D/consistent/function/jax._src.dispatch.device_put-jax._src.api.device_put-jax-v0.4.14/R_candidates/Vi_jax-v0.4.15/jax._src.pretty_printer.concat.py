def concat(docs: Sequence[Doc]) -> Doc:
  """Concatenation of documents."""
  docs = list(docs)
  if len(docs) == 1:
    return docs[0]
  return _ConcatDoc(docs)
