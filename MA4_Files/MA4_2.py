#!/usr/bin/env python3.9

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

def fib_threading_cpp(lst, p, n):
	tick = pc()
	p.fib()
	lst.append((n, pc()-tick))

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

	for n in range(30, 46, 5):
		print(f"n-value: {n}")
		tick = pc()

		p1 = mp.Process(target = fib_threading_py, args = (fp, fib_py, n))

		p2 = mp.Process(target = fib_threading_py, args = (fn, fib_numba, n))

		f = Person(n)

		p3 = mp.Process(target = fib_threading_cpp, args = (fc, f, n))

		for p in [p1, p2, p3]:
			p.start()

		for p in [p1, p2, p3]:
			p.join()

		print(f"total time for {n}: {pc()-tick}")

	plotting(fp, fn, fc)

if __name__ == '__main__':
	main()
