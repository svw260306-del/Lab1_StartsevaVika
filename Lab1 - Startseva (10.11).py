import numpy as np
import os
# ЗАДАЧА 1
# Подзадача 1.1
# Создайте массив float32 со значениями [0.1, 0.2, 0.3] и вычислите сумму. Сравните с точным значением
a32 = np.array([0.1, 0.2, 0.3], dtype=np.float32)
a64 = np.array([0.1, 0.2, 0.3], dtype=np.float64)
print(f"a32 сумма: {a32.sum()}")
print(f"a64 сумма: {a64.sum()}")


# Подзадача 1.2
# Найдите машинное эпсилон для float32 и float64 с помощью np.finfo
f32 = np.finfo(np.float32)
f64 = np.finfo(np.float64)
print("------ float32 ----- \neps =", f32.eps, "\nmin =", f32.min, "\nmax =", f32.max)
print("==============================\n----------- float64 ---------- \neps =", f64.eps, "\nmin =", f64.min, "\nmax =", f64.max)


# Подзадача 1.3
# Продемонстрируйте эффект потери точности при вычитании близких чисел (катастрофическая отмена)
x = np.float32(1.0000001)
print(np.float32(1.0000001) - np.float32(1.0))
y = np.float64(1e20)
print((y + np.float64(1)) - y)


# ЗАДАЧА 2
# Подзадача 2.1
# Создайте массив A формы (4, 5). Получите: все элементы второй строки, столбец с индексом 3, подмассив из строк 1-3 и столбцов 2-4
A = np.arange(20).reshape(4, 5) + 1
print("--- элементы 2 стр ---")
print(A[1, :])
print("--- столбец с индексом 3 ---")
print(A[:, 3])
print("--- строки 1-3, столбцы 2-4 ---")
print(A[1:4, 2:5])  # строки 1-3, столбцы 2-4


# Подзадача 2.2
# С помощью fancy-индексации выберите элементы с индексами [0, 2, 3] по строкам и [1, 4] по столбцам
print(A[[0, 2, 3]][:, [1, 4]])


# Подзадача 2.3
# Используя логическую индексацию, замените все отрицательные элементы массива на 0
D = np.array([[-1,  2, -3,  4, -5],
              [ 6, -7,  8, -9, 10],
              [-11, 12, -13, 14, -15],
              [ 16, -17, 18, -19, 20]])
D[D < 0] = 0
print(D)


# Подзадача 2.4
# Продемонстрируйте broadcasting: создайте массив B формы (4, 1) и массив C формы (1, 5). Сложите их без циклов
B = np.arange(4).reshape(4, 1)   
C = np.arange(5).reshape(1, 5)
print("--- Массив B ---\n", B)
print("--- Массив C ---\n", C)
print("--- Массив суммы ---\n",B + C)


# ЗАДАЧА 3
# Подзадача 3.1
# Создайте на диске memory-mapped файл для массива формы (1000, 1000) типа float64. Заполните его случайными числами
filename = 'test_mmap_check.dat'
if os.path.exists(filename):
    os.remove(filename)
try:
    arr = np.memmap(filename, dtype='float64', mode='w+', shape=(100, 100))
    arr[:] = np.random.rand(100, 100)
    # Пробуем flush
    arr.flush()
    print("flush() успешно выполнен")
    del arr
except OSError as e:
    print(f"Ошибка: {e}")
    print("Среда, вероятно, не поддерживает memmap.flush() корректно.")


# Подзадача 3.2
# Прочитайте отдельный столбец и строку из этого файла (без загрузки всего массива)
import time
ROWS, COLS = 2000, 2000
dtype = np.float32
filename = "small_array.dat"
if not os.path.exists(filename):
    print("Создаём файл по одной строке...")
    arr = np.memmap(filename, dtype=dtype, mode='w+', shape=(ROWS, COLS))
    for i in range(ROWS):
        arr[i, :] = np.arange(i * COLS, (i + 1) * COLS, dtype=dtype)
    arr.flush()
    del arr
    print("Файл создан.")
else:
    print("Файл уже есть.")
arr = np.memmap(filename, dtype=dtype, mode='r', shape=(ROWS, COLS))
row_idx, col_idx = 100, 200
row = arr[row_idx, :]
col = arr[:, col_idx]
print(f"Строка {row_idx}: {row[:5]}")
print(f"Столбец {col_idx}: {col[:5]}")
n = 100
t0 = time.perf_counter()
sum_rows = sum(arr[i, :].sum() for i in range(n))
time_rows = time.perf_counter() - t0
t0 = time.perf_counter()
sum_cols = sum(arr[:, j].sum() for j in range(n))
time_cols = time.perf_counter() - t0
print(f"Сумма по {n} строкам: {sum_rows:.2f}, время: {time_rows:.4f} сек")
print(f"Сумма по {n} столбцам: {sum_cols:.2f}, время: {time_cols:.4f} сек")
print(f"Ускорение по строкам: {time_cols / time_rows:.1f}x")
del arr


# Подзадача 3.2
# Сравните время обхода массива по строкам (row-major) и по столбцам (column-major) с использованием %timeit. Объясните результат.
ROWS, COLS = 4000, 4000
dtype = np.float32
filename = "demo_array.dat"
if not os.path.exists(filename):
    print("Создаём файл на диске (поблочно, без большого массива в RAM)...")
    arr = np.memmap(filename, dtype=dtype, mode='w+', shape=(ROWS, COLS))
    for i in range(ROWS):
        arr[i, :] = np.arange(i * COLS, (i + 1) * COLS, dtype=dtype)
    arr.flush()
    del arr
    print("Файл создан.")
else:
    print("Файл уже есть.")
arr = np.memmap(filename, dtype=dtype, mode='r', shape=(ROWS, COLS))
def sum_rows(a, n=200):
    s = 0.0
    for i in range(n):
        s += a[i, :].sum()
    return s
def sum_cols(a, n=200):
    s = 0.0
    for j in range(n):
        s += a[:, j].sum()
    return s
n = 200
t0 = time.perf_counter()
for _ in range(10):
    sum_rows(arr, n)
t1 = time.perf_counter()
t2 = time.perf_counter()
for _ in range(10):
    sum_cols(arr, n)
t3 = time.perf_counter()
print(f"Время 10 прогонов sum_rows: {t1 - t0:.4f} сек")
print(f"Время 10 прогонов sum_cols: {t3 - t2:.4f} сек")
print(f"Ускорение при обходе по строкам: {(t3 - t2) / (t1 - t0):.1f}x")
del arr


# Подзадача 4.1
# Создать разреженную матрицу (5, 5), плотность ~20%, формат CSR
from scipy.sparse import random, csr_matrix, coo_matrix, csc_matrix
A_csr = random(5, 5, density=0.2, format='csr', random_state=42)
print("CSR матрица (5x5, плотность 20%):\n-----------------------------------------------------------\n", A_csr.toarray())


# Подзадача 4.2
# Преобразуйте её в COO и CSC
A_coo = A_csr.tocoo()
A_csc = A_csr.tocsc()
print("COO формат (nnz={}):".format(A_coo.nnz), "\n-----------------------------------------------------------------")
print("   Rows:", A_coo.row)
print("   Cols:", A_coo.col)
print("   Vals:", A_coo.data)
print("=================================================================\nCSC формат (nnz={}):".format(A_csc.nnz), "\n-----------------------------------------------------------------")
print("   Indptr:", A_csc.indptr)
print("   Indices:", A_csc.indices)
print("   Data:", A_csc.data)


# Подзадача 4.3
# Выполните умножение разреженной матрицы на плотный вектор
N, dens = 1000, 0.01
A_sparse = random(N, N, density=dens, format='csr', random_state=42)
A_dense = A_sparse.toarray()
v_large = np.ones(N)
t0 = time.perf_counter()
for _ in range(100):
    A_sparse.dot(v_large)
t_sparse = time.perf_counter() - t0
t0 = time.perf_counter()
for _ in range(100):
    A_dense @ v_large
t_dense = time.perf_counter() - t0
print(f"Время разреженного умножения (100 итераций):   |   {t_sparse:.4f} сек")
print(f"Время плотного умножения (100 итераций):       |   {t_dense:.4f} сек")
if t_sparse > 0:
    print(f"Ускорение разреженного метода:                 |   {t_dense / t_sparse:.1f}x")


    # Подзадача 4.4
# Сравните время умножения разреженной и плотной матриц при большой размерности (например, 1000×1000 с плотностью 0.01)
N, dens = 1000, 0.01
rng = np.random.default_rng(42)
total_nnz = int(N * N * dens)
indices_flat = rng.choice(N * N, size=total_nnz, replace=False)
rows_idx = indices_flat // N
cols_idx = indices_flat % N
data = rng.random(total_nnz)
sort_order = np.argsort(rows_idx)
csr_indices = cols_idx[sort_order]
csr_data = data[sort_order]
sorted_rows = rows_idx[sort_order]
csr_indptr = np.zeros(N + 1, dtype=int)
row_counts = np.bincount(sorted_rows, minlength=N)
csr_indptr[1:] = np.cumsum(row_counts)
A_dense = np.zeros((N, N))
for i in range(N):
    start = csr_indptr[i]
    end = csr_indptr[i+1]
    if start < end:
        A_dense[i, csr_indices[start:end]] = csr_data[start:end]
v_large = np.ones(N)
t0 = time.perf_counter()
iterations = 100
for _ in range(iterations):
    res_s = np.zeros(N)
    for i in range(N):
        start = csr_indptr[i]
        end = csr_indptr[i+1]
        if start < end:
            res_s[i] = np.sum(csr_data[start:end] * v_large[csr_indices[start:end]])
t_sparse = time.perf_counter() - t0
t0 = time.perf_counter()
for _ in range(iterations):
    res_d = A_dense @ v_large
t_dense = time.perf_counter() - t0
print(f"Размер матрицы: {N}x{N}, плотность: {dens}", "\n-------------------------------------------------------------")
print(f"Время разреженного умножения ({iterations} итераций):   |   {t_sparse:.4f} сек")
print(f"Время плотного умножения ({iterations} итераций):       |   {t_dense:.4f} сек")
if t_sparse > 0:
    print(f"Ускорение разреженного метода:                 |   {t_dense / t_sparse:.1f}x")



# Подзадача 5.1
# Напишите функцию на Python, которая вычисляет сумму квадратов элементов списка


# Подзадача 5.2
# Напишите аналогичную функцию на Cython (в отдельном файле .pyx) и скомпилируйте её


# Подзадача 5.3
# Сравните время выполнения обеих функций на массиве из 10⁷ элементов
