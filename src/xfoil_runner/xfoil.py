import os
import subprocess
import numpy as np
import sys
import matplotlib.pyplot as plt

"""
Baseado em https://github.com/JARC99/xfoil-runner e https://www.youtube.com/watch?v=zGZin_PPLdc.

Outros materiais:
https://github.com/karanchawla/Airfoil-Optimization/tree/master/xfoil
"""


def run_xfoil(airfoil_path, airfoil_name="Default Airfoil", alpha_i=0, alpha_f=10, alpha_step=0.25, Re=1000000, n_iter=100, polar_path="src/xfoil_runner/data/genome_polar.txt"):

    if sys.platform.startswith('win32'):
        XFOIL_BIN = "xfoil.exe"
    elif sys.platform.startswith('darwin'):
        XFOIL_BIN = "xfoil"
    elif sys.platform.startswith('linux'):
        XFOIL_BIN = "xfoil"

    """ Gera o arquivo de input para o XFOIL"""
    if os.path.exists(polar_path):
        os.remove(polar_path)

    with open("src/xfoil_runner/data/input_file.in", 'w') as file:
        file.write(f"LOAD {airfoil_path}\n")
        file.write(airfoil_name + '\n')
        file.write("PANE\n")
        file.write("OPER\n")
        file.write("Visc {0}\n".format(Re))
        file.write("PACC\n")
        file.write(f"{polar_path}\n\n")
        file.write("ITER {0}\n".format(n_iter))
        file.write("ASeq {0} {1} {2}\n".format(alpha_i, alpha_f,
                                               alpha_step))
        file.write("\n\n")
        file.write("quit\n")

    subprocess.call(
        f"{XFOIL_BIN} < src/xfoil_runner/data/input_file.in", shell=True)

    polar_data = np.loadtxt(polar_path, skiprows=12)


def plot_polar(axs, polar_path="src/xfoil_runner/data/genome_polar.txt"):
    """
    Plot Cl/alpha, Cd/alpha and Cl/Cd and Cl^3/Cd^2 from a certain analysis.
    :param polar_txt: .txt file where xfoil polar data is stored.
    """
    with open(polar_path) as file:
        data = np.array([np.array([float(x) for x in line.split()])
                        for line in file.readlines()[12:]])
        alpha = data[:, 0]
        Cl = data[:, 1]
        Cd = data[:, 2]
        Cl3Cd2 = Cl**3 / Cd**2

    axs[0, 0].plot(alpha, Cl)
    axs[0, 0].set(xlabel=r'$\alpha$ [-]', ylabel='$C_{l}$')

    axs[0, 1].plot(alpha, Cd)
    axs[0, 1].set(xlabel=r'$\alpha$ [-]', ylabel='$C_{d}$')

    axs[1, 0].plot(Cd, Cl)
    axs[1, 0].set(xlabel=r'$C_{d}$', ylabel='$C_{l}$')

    axs[1, 1].plot(alpha, Cl3Cd2)
    axs[1, 1].set(xlabel=r'$\alpha$',
                  ylabel='$C_{l}^{3}/C_{d}^{2}$ [-]')


def _example():
    run_xfoil("airfoils/generated_airfoil.dat", "Gen_Airfoil")
    plot_polar()


"""Se esse arquivo for executado, rode _example()"""
if __name__ == "__main__":
    _example()
