import time
import numpy as np
from sum_squares_python import sum_squares_python
from sum_squares_cython import sum_squares_cython
N = 10_000_000 
arr_list = list(range(N))
arr_np = np.arange(N, dtype=np.int64)
start = time.perf_counter()
res_py = sum_squares_python(arr_list)
time_py = time.perf_counter() - start
start = time.perf_counter()
res_cy = sum_squares_cython(arr_np)
time_cy = time.perf_counter() - start
print(f"Размер массива: {N:,}")
print(f"Результаты совпадают: {res_py == res_cy}")
print(f"Время Python     |     {time_py:.4f} сек")
print(f"Время Cython     |     {time_cy:.4f} сек")
if time_cy > 0:
    print(f"Ускорение             |     {time_py / time_cy:.1f}x")
