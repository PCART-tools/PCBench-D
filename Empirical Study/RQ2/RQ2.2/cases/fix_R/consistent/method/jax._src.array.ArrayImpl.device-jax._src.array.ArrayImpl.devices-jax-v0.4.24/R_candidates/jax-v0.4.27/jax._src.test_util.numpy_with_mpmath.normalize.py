  def normalize(self, exact, reference, value):
    """Normalize reference and value using precision defined by the
    difference of exact and reference.
    """
    def worker(ctx, s, e, r, v):
      ss, sm, se, sbc = s._mpf_
      es, em, ee, ebc = e._mpf_
      rs, rm, re, rbc = r._mpf_
      vs, vm, ve, vbc = v._mpf_

      if not (ctx.isfinite(e) and ctx.isfinite(r) and ctx.isfinite(v)):
        return r, v

      me = min(se, ee, re, ve)

      # transform mantissa parts to the same exponent base
      sm_e = sm << (se - me)
      em_e = em << (ee - me)
      rm_e = rm << (re - me)
      vm_e = vm << (ve - me)

      # find matching higher and non-matching lower bits of e and r
      sm_b = bin(sm_e)[2:] if sm_e else ''
      em_b = bin(em_e)[2:] if em_e else ''
      rm_b = bin(rm_e)[2:] if rm_e else ''
      vm_b = bin(vm_e)[2:] if vm_e else ''

      m = max(len(sm_b), len(em_b), len(rm_b), len(vm_b))
      em_b = '0' * (m - len(em_b)) + em_b
      rm_b = '0' * (m - len(rm_b)) + rm_b

      c1 = 0
      for b0, b1 in zip(em_b, rm_b):
        if b0 != b1:
          break
        c1 += 1
      c0 = m - c1

      # truncate r and v mantissa
      rm_m = rm_e >> c0
      vm_m = vm_e >> c0

      # normalized r and v
      nr = ctx.make_mpf((rs, rm_m, -c1, len(bin(rm_m)) - 2)) if rm_m else (-ctx.zero if rs else ctx.zero)
      nv = ctx.make_mpf((vs, vm_m, -c1, len(bin(vm_m)) - 2)) if vm_m else (-ctx.zero if vs else ctx.zero)

      return nr, nv

    ctx = exact.context
    scale = abs(exact)
    if isinstance(exact, ctx.mpc):
      rr, rv = worker(ctx, scale, exact.real, reference.real, value.real)
      ir, iv = worker(ctx, scale, exact.imag, reference.imag, value.imag)
      return ctx.make_mpc((rr._mpf_, ir._mpf_)), ctx.make_mpc((rv._mpf_, iv._mpf_))
    elif isinstance(exact, ctx.mpf):
      return worker(ctx, scale, exact, reference, value)
    else:
      assert 0  # unreachable
