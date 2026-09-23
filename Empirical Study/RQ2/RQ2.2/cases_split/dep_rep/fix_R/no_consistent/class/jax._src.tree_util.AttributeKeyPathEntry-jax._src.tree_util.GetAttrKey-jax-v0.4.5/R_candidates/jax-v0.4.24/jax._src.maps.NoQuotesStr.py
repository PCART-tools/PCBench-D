class NoQuotesStr(str):
  __repr__ = str.__str__
