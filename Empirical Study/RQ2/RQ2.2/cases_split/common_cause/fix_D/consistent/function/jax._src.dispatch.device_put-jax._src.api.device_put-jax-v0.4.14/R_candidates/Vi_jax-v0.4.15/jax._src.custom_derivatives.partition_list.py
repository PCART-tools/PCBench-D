def partition_list(choice, lst):
  out = [], []
  which = [out[choice(elt)].append(elt) or choice(elt) for elt in lst]
  def merge(l1, l2):
    i1, i2 = iter(l1), iter(l2)
    return [next(i2 if snd else i1) for snd in which]
  return out, merge
