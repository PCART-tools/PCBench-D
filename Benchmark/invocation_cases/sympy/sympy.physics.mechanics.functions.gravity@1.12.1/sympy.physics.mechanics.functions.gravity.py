import sympy as sp
import inspect
from sympy.physics.mechanics.functions import gravity, Particle
from sympy.physics.vector import ReferenceFrame, Point

def main():
    m, g = sp.symbols('m g')
    N = ReferenceFrame('N')

    P = Point('P')
    P.set_vel(N, 0)
    pa = Particle('pa', P, m)
    grav = gravity(g * N.y, pa)

    print("gravity result:", grav)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(gravity))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()