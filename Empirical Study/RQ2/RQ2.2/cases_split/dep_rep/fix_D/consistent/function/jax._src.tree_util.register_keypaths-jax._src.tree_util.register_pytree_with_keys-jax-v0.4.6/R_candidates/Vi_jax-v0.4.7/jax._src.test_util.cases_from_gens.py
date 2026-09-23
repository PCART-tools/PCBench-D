def cases_from_gens(*gens):
  sizes = [1, 3, 10]
  cases_per_size = int(FLAGS.jax_num_generated_cases / len(sizes)) + 1
  for size in sizes:
    for i in range(cases_per_size):
      yield (f'_{size}_{i}',) + tuple(gen(size) for gen in gens)
