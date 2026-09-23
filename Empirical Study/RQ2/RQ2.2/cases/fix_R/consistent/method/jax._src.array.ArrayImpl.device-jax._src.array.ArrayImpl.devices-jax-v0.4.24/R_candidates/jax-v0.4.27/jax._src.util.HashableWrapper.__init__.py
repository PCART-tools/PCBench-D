  def __init__(self, x):
    self.x = x
    try: self.hash = hash(x)
    except: self.hash = None
