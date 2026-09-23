import inspect
from sympy.tensor.tensor import (
    TensorIndexType, tensor_indices,
    TensorType, tensorsymmetry, Tensor
)

def main():
    Lorentz = TensorIndexType('Lorentz')
    i, j, k, l = tensor_indices('i j k l', Lorentz)
    sym = tensorsymmetry([1, 1])
    Ttype = TensorType([Lorentz, Lorentz], sym)
    A = Ttype('A')
    B = Ttype('B')
    t = A(i, k) * B(-k, -j)
    t2 = Tensor.fun_eval(t,(i, k), (-j, l))
    print(t2)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Tensor.fun_eval))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
