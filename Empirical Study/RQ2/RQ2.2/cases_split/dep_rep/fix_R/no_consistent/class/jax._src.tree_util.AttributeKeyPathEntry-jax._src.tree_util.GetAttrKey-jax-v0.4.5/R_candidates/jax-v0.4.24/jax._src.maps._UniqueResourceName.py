class _UniqueResourceName:
  def __init__(self, uid, tag=None):
    self.uid = uid
    self.tag = tag
  def __eq__(self, other):
    return type(other) is _UniqueResourceName and self.uid == other.uid
  def __hash__(self):
    return hash(self.uid)
  def __repr__(self):
    return f"<UniqueResource {self.tag} {self.uid}>"
