import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from math import radians

g = -9.81


class Pilka:
    # na razie "działa" część od rzutu pionowego
    # może niedługo  piłka będzie się poruszać w dwóch wymiarach, pod zadanym kątem początkowym
    def __init__(self, v0, h0, kat):
        self.vx = 0.3                       # [m/s], prędkość pozioma //np.cos(radians(kat%90)) * v0
        self.vy = np.sin(radians(kat%90)) * v0       # [m/s], prędkość pionowa
        self.x = 0                          # [m], położenie w poziomoie
        self.y = h0                         # [m], wysokość; równoznaczne z h, ale na wykresie lepsze jest y (chyba)
        self.hmax = self.vy**2 / 2*(-g)     # [m], maksymalna wysokość, na jaką może wznieść się piłka


def aktualizuj_pilke(x_stare, y_stare, vx_stare, vy_stare, t, dt):
    # uaktualnienie położenia x i y oraz prędkości vy stosując algorytm skokowy
    # pierwsza część ruchu / pierwsza połowa dt
    x_pol = x_stare + vx_stare * 0.5*dt
    y_pol = y_stare + vy_stare * 0.5*dt

    # aktualizacja prędkości
    vx_nowe = vx_stare #+ g * dt
    vy_nowe = vy_stare + g * dt

    # druga część ruchu / druga połowa dt
    x_nowe = x_pol + vx_nowe * 0.5*dt
    y_nowe = y_pol + vy_nowe * 0.5*dt

    # sprawdzanie czy piłka nie no-clip'uje przez podłogę
    # jeśli tak, to robimy krok czasowy trochę mniejszsy, żeby akurat trafić w położenie y=0
    if y_nowe < 0:
        y_nowe = 0
        # poniżej liczenie czasu dt, po którym nastąpi odbicie od podłogi
        dt_hop = (vy_stare + np.sqrt(vy_stare**2 + 2*g*y_stare)) / g
        vy_nowe = -(vy_stare + g * dt_hop)
        x_nowe = x_stare + vx_stare * dt_hop
        t += dt_hop
    else:
        t += dt

    return x_nowe, y_nowe, vx_nowe, vy_nowe, t


def main():
    v0 = 20     #input("Podaj prędkość początkową wyrzuconej piłki:")
    kat = 60    #input("Podaj kąt rzucenia piłki:")
    h0 = 0      #input("Podaj wysokość początkową piłki:")
    dt = 0.1    #input("Podaj czas, po którym wartości mają być aktualizowane:")
    tmax = 15   #input("Podaj maksymalny czas trwania symulacji:")
    pilka = Pilka(v0, h0, kat)

    t = 0
    t_list, y_list =[], []  # listy, do których po każdej iteracji będą zapisywane obecny czas i wysokość

    while t <= tmax:
        pilka.x, pilka.y, pilka.vx, pilka.vy, t = aktualizuj_pilke(pilka.x, pilka.y, pilka.vx, pilka.vy, t, dt)
        t_list.append(t)
        y_list.append(pilka.y)

    # wykres wysokości od czasu
    fig, ax = plt.subplots()
    ax.plot(t_list, y_list)
    plt.title("Wykres zależności wysokości piłki h od upływu czasu t")
    plt.xlabel("t [s]")
    plt.ylabel("h [m]")
    plt.show()


if __name__ == "__main__":
    main()
