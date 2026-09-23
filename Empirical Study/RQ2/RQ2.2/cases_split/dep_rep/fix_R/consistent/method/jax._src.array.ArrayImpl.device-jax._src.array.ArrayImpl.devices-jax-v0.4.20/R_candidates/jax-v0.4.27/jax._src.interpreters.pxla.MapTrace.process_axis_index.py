  def process_axis_index(self, frame):
    bind = HashableFunction(
        lambda _: jax.lax.axis_index(frame.name),
        (jax.lax.axis_index, frame.name))
    fake_primitive = FakePrimitive(multiple_results=False, bind=bind)
    with core.eval_context():
      range = jax.lax.iota(np.int32, frame.size)
    dummy_tracer = MapTracer(self, range, {frame.name: 0})
    return self.process_primitive(fake_primitive, (dummy_tracer,), {})
