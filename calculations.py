import numpy as np

class KrzywaCalculations:
    def find_a(self, L, s):
        def func(a_guess):
            return 2 * a_guess * np.sinh(L / (2 * a_guess)) - s

        a_min, a_max = 0.1, 100
        while (a_max - a_min) > 0.0001:
            a = (a_min + a_max) / 2
            if func(a) > 0:
                a_max = a
            else:
                a_min = a
        return (a_min + a_max) / 2

    def calculate_forces(self, a, L, w):
        T_max = w * a
        angle = np.arcsinh(L / (2 * a))
        return T_max

    def generate_x(self, L):
        return np.linspace(0, L, 1000)

    def generate_y(self, a, L, h, x):
        return a * np.cosh((x - L / 2) / a) - a * np.cosh(L / (2 * a)) + h