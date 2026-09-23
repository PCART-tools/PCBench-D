def _get_example_iter(inputs):
  dataset = dataset_ops.Dataset.from_tensor_slices(inputs)
  return dataset_ops.make_one_shot_iterator(dataset)
