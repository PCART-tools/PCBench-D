def fmod(g, input, other):
    return g.op("Mod", input, other, fmod_i=1)
