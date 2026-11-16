cpdef long long sum_squares_cython(long[:] arr):
    cdef long long total = 0
    cdef Py_ssize_t i
    cdef long n = arr.shape
    for i in range(n):
        total += arr[i] * arr[i]
    return total
