#!/usr/bin/env python3.9

import concurrent.futures as future

import multiprocessing as mp

from numba import njit
from time import perf_counter as pc
from matplotlib import pyplot as plt

from person import Person

def fib_py(n):
	if n <= 1:
		return n
	else:
		return (fib_py(n-1) + fib_py(n-2))

@njit
def fib_numba(n):
	if n <= 1:
		return n
	else:
		return (fib_numba(n-1) + fib_numba(n-2))

def fib_threading_py(lst, func, n):
	tick = pc()
	func(n)
	lst.append((n, pc()-tick))
	print(lst)

	return lst

def fib_threading_cpp(lst, p, n):
	tick = pc()
	p.fib()
	lst.append((n, pc()-tick))
	return lst

def plotting(fp, fn, fc):
	for f in [fp ,fn, fc]:
		for coord in f:
			plt.plot(coord[0],coord[1])
	plt.xlabel("n-values")
	plt.ylabel("time")
	plt.title("")
	#plt.legend()

	plt.savefig("plot.png")	


def main():

	fp = []
	fn = []
	fc = []

	for n in range(30, 39, 5):
		print(f"n-value: {n}")
		tick = pc()

		with future.ProcessPoolExecutor() as ex:
			p1 = ex.submit(fib_threading_py, fp, fib_py, n)

			p2 = ex.submit(fib_threading_py, fn, fib_numba, n)

			f = Person(n)

			p3 = ex.submit(fib_threading_cpp, fc, f, n)

			fp = p1.result()
			fn = p2.result()
			fc = p3.result()

		print(f"total time for {n}: {pc()-tick}")
		print(fp)

	plotting(fp, fn, fc)

if __name__ == '__main__':
	main()
