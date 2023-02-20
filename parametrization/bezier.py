import bezier_aux as aux
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv


class bezier_airfoil:

    all = []

    def __init__(self, dat: str):
        """ Converte o .dat para coordenadas np.array X e Y """
        self.dat = dat
        df = read_csv(dat, names=("X", "Y"), sep='\s+')
        self.original_name = df.iloc[0]["X"]  # Nome do perfil importado
        self.X = df["X"].drop(0).to_numpy(float)
        self.Y = df["Y"].drop(0).to_numpy(float)

    def set_X(self, xvalue):
        self.X = xvalue

    def set_Y(self, yvalue):
        self.Y = yvalue

    def get_bezier_parameters(self, degree=3):
        """ 
        Args:

        degree: degree of the Bézier curve. 2 for quadratic, 3 for cubic.

        Based on https://stackoverflow.com/questions/12643079/b%C3%A9zier-curve-fitting-with-scipy
        and probably on the 1998 thesis by Tim Andrew Pastva, "Bézier Curve Fitting".
        """
        self.degree = degree

        if self.degree < 1:
            raise ValueError('degree must be 1 or greater.')

        if len(self.X) != len(self.Y):
            raise ValueError('X and Y must be of the same length.')

        if len(self.X) < self.degree + 1:
            raise ValueError(f'There must be at least {self.degree + 1} points to '
                             f'determine the parameters of a degree {self.degree} curve. '
                             f'Got only {len(self.X)} points.')

        T = np.linspace(0, 1, len(self.X))
        M = aux.bmatrix(T, self.degree)
        points = np.array(list(zip(self.X, self.Y)))

        parameters = aux.least_square_fit(points, M).tolist()
        parameters[0] = [self.X[0], self.Y[0]]
        parameters[len(parameters)-1] = [self.X[len(self.X)-1],
                                         self.Y[len(self.Y)-1]]

        return parameters

    def __str__(self):
        return (""
                .format())


def _example():
    airfoil = bezier_airfoil("airfoils/s1223.dat")
    # airfoil.set_X(np.linspace(0, 15))
    # airfoil.set_Y(np.cos(np.linspace(0, 15)))
    params = airfoil.get_bezier_parameters(4)  # Args: Grau do polinômio

    plt.plot(airfoil.X, airfoil.Y, "ro", label='Original Points')

    x_params = [param[0] for param in params]
    y_params = [param[1] for param in params]

    # Plot the control points
    plt.plot(x_params, y_params, 'k--o', label='Control Points')

    # Plot the resulting Bezier curve
    xvals, yvals = aux.generate_bezier_curve(params, nTimes=1000)
    plt.plot(xvals, yvals, 'b-', label='Bezier')

    plt.legend()
    plt.show()

    # Se esse arquivo for executado, rode _example()
if __name__ == "__main__":
    _example()