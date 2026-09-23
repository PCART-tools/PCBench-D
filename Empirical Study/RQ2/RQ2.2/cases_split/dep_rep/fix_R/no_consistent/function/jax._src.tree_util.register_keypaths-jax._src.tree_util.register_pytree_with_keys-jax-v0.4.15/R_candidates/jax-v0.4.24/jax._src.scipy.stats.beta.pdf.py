@implements(osp_stats.beta.pdf, update_doc=False)
def pdf(x: ArrayLike, a: ArrayLike, b: ArrayLike,
        loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  return lax.exp(logpdf(x, a, b, loc, scale))
