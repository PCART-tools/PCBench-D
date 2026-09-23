import sympy
from sympy.polys.domains import ZZ, FF
from sympy.polys.domains.modularinteger import ModularInteger
import inspect

def main():
    modulus = 7
    value = 3
    mod_int = FF(modulus)(value)

    result = ModularInteger.to_int(mod_int)
    print("to_int result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ModularInteger.to_int))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()