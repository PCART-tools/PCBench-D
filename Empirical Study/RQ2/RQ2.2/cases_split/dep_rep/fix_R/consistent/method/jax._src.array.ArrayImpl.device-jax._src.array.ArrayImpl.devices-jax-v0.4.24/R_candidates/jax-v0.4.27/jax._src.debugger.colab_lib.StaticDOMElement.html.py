  def html(self):
    attr_str = ""
    if self.attrs:
      attr_str = " " + (" ".join(
          [f"{key}=\"{value}\"" for key, value in self.attrs.items()]))
    children = []
    children = "\n".join([str(c) for c in self.children])
    return f"<{self.name}{attr_str}>{children}</{self.name}>"
