    class backend_mod(matplotlib.backend_bases._Backend):
        locals().update(vars(importlib.import_module(backend_name)))
