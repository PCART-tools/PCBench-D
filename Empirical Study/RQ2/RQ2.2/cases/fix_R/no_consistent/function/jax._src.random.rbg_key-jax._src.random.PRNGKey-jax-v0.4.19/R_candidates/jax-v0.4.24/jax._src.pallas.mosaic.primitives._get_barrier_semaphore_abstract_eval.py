@get_barrier_semaphore_p.def_abstract_eval
def _get_barrier_semaphore_abstract_eval():
  return pl_core.AbstractMemoryRef(
      jax_core.ShapedArray((), tpu_core.BarrierSemaphoreTy()),
      tpu_core.TPUMemorySpace.SEMAPHORE,
  )
