def _pad(arr, pads, pad_value):
  out = np.pad(arr, np.maximum(0, pads), mode='constant',
                constant_values=pad_value).astype(arr.dtype)
  slices = tuple(_slice(abs(lo) if lo < 0 else 0, hi % dim if hi < 0 else None)
                 for (lo, hi), dim in zip(pads, np.shape(arr)))
  return out[slices]
