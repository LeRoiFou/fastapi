from typing import Tuple

def my_function(a:float, b:float) -> Tuple[float, float, float]:
    return a + b, a - b, a * b

res1, res2, res3 = my_function(5, 2)
print(res1)
print(res2)
print(res3)
