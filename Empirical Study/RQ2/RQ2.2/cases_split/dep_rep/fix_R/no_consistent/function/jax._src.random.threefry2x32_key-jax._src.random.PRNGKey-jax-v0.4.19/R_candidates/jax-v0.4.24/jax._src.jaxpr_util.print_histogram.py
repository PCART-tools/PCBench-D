def print_histogram(histogram: dict[Any, int]):
  count_width = max(len(str(v)) for v in histogram.values())
  count_fmt = '{:>' + str(count_width) + 'd}'
  pairs = [(v, k) for k, v in histogram.items()]
  for count, name in sorted(pairs, reverse=True):
    print(count_fmt.format(count), name)
