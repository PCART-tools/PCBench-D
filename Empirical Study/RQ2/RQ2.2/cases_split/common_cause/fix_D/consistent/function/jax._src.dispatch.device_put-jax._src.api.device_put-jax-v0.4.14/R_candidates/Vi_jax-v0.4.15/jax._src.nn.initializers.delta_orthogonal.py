@export
def delta_orthogonal(
  scale: RealNumeric = 1.0,
  column_axis: int = -1,
  dtype: DTypeLikeInexact = jnp.float_) -> Initializer:
  """
  Builds an initializer for delta orthogonal kernels.

  Args:
    scale: the upper bound of the uniform distribution.
    column_axis: the axis that contains the columns that should be orthogonal.
    dtype: the default dtype of the weights.

  Returns:
    A `delta orthogonal initializer`_. The shape passed to the initializer must
    be 3D, 4D, or 5D.

  Example:

  >>> import jax, jax.numpy as jnp
  >>> initializer = jax.nn.initializers.delta_orthogonal()
  >>> initializer(jax.random.PRNGKey(42), (3, 3, 3), jnp.float32)  # doctest: +SKIP
  Array([[[ 0.        ,  0.        ,  0.        ],
          [ 0.        ,  0.        ,  0.        ],
          [ 0.        ,  0.        ,  0.        ]],
  <BLANKLINE>
         [[ 0.27858758, -0.7949833 , -0.53887904],
          [ 0.9120717 ,  0.04322892,  0.40774566],
          [-0.30085585, -0.6050892 ,  0.73712474]],
  <BLANKLINE>
         [[ 0.        ,  0.        ,  0.        ],
          [ 0.        ,  0.        ,  0.        ],
          [ 0.        ,  0.        ,  0.        ]]], dtype=float32)


  .. _delta orthogonal initializer: https://arxiv.org/abs/1806.05393
  """
  def init(key: KeyArray,
           shape: core.Shape,
           dtype: DTypeLikeInexact = dtype) -> Array:
    dtype = dtypes.canonicalize_dtype(dtype)
    if len(shape) not in [3, 4, 5]:
      raise ValueError("Delta orthogonal initializer requires a 3D, 4D or 5D "
                       "shape.")
    if shape[-1] < shape[-2]:
      raise ValueError("`fan_in` must be less or equal than `fan_out`. ")
    ortho_init = orthogonal(scale=scale, column_axis=column_axis, dtype=dtype)
    ortho_matrix = ortho_init(key, shape[-2:])
    W = jnp.zeros(shape, dtype=dtype)
    if len(shape) == 3:
      k = shape[0]
      return W.at[(k-1)//2, ...].set(ortho_matrix)
    elif len(shape) == 4:
      k1, k2 = shape[:2]
      return W.at[(k1-1)//2, (k2-1)//2, ...].set(ortho_matrix)
    else:
      k1, k2, k3 = shape[:3]
      return W.at[(k1-1)//2, (k2-1)//2, (k3-1)//2, ...].set(ortho_matrix)
  return init
