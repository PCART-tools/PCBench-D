  def __init__(self):
    self.gensym = core.gensym()
    self.tracer_to_var = {}
    self.constid_to_tracer = {}
    self.constvar_to_val = {}
    self.tracers = []   # circ refs, frame->tracer->trace->main->frame,
    self.eqns = []      # cleared when we pop frame from main
    self.invars = []
    self.effects = set()
    self.attrs_tracked = []
    self.attrs_inits = []
    self.attrs_vars = []
    self.debug_info = None
