def _rng_algorithm(algorithm: RandomAlgorithm):
  if algorithm == RandomAlgorithm.RNG_THREE_FRY:
    return mhlo.RngAlgorithmAttr.get("THREE_FRY")
  elif algorithm == RandomAlgorithm.RNG_PHILOX:
    return mhlo.RngAlgorithmAttr.get("PHILOX")
  elif algorithm == RandomAlgorithm.RNG_DEFAULT:
    return mhlo.RngAlgorithmAttr.get("DEFAULT")
  else:
    assert False
