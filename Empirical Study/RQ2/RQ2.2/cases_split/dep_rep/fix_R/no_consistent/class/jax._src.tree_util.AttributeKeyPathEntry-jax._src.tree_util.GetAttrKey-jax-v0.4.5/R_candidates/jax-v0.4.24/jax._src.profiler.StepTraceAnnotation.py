class StepTraceAnnotation(TraceAnnotation):
  """Context manager that generates a step trace event in the profiler.

  The step trace event spans the duration of the code enclosed by the context.
  The profiler will provide the performance analysis for each step trace event.

  For example, it can be used to mark training steps and enable the profiler to
  provide the performance analysis per step:

  >>> while global_step < NUM_STEPS:                                           # doctest: +SKIP
  ...   with jax.profiler.StepTraceAnnotation("train", step_num=global_step):  # doctest: +SKIP
  ...     train_step()                                                         # doctest: +SKIP
  ...     global_step += 1                                                     # doctest: +SKIP

  This will cause a "train xx" event to show up on the trace timeline if the
  event occurs while the process is being traced by TensorBoard. In addition,
  if using accelerators, the device trace timeline will also show a "train xx"
  event. Note that "step_num" can be set as a keyword argument to pass the
  global step number to the profiler.

  """

  def __init__(self, name: str, **kwargs):
    super().__init__(name, _r=1, **kwargs)
