def next_power_of_2(x: int) -> int:
  if x == 0:
    return 1
  return int(2 ** math.ceil(math.log2(x)))
