import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

g = -9.81


class Pilka:
    # na razie "działa" część od rzutu pionowego
    # może niedługo  piłka będzie się poruszać w dwóch wymiarach, pod zadanym kątem początkowym
    def __init__(self, v0, h0, kat):
        self.vx = 0.3                       # [m/s], prędkość pozioma //np.cos(kat%90) * v0
        self.vy = np.sin(kat%90) * v0       # [m/s], prędkość pionowa
        self.x = 0                          # [m], położenie w poziomoie
        self.y = h0                         # [m], wysokość; równoznaczne z h, ale na wykresie lepsze jest y (chyba)
        self.hmax = self.vy**2 / 2*(-g)     # [m], maksymalna wysokość, na jaką może wznieść się piłka


def aktualizuj_pilke(x_stare, y_stare, vx_stare, vy_stare, t, dt):
    # uaktualnienie położenia x i y oraz prędkości vy - niech vx będzie na razie stałe
    vx_nowe = vx_stare #+ g * dt
    vy_nowe = vy_stare + g * dt
    x_nowe = x_stare + vx_stare * dt
    y_nowe = y_stare + vy_stare * dt

    # sprawdzanie czy piłka nie no-clip'uje przez podłogę
    # jeśli tak, to robimy krok czasowy trochę mniejszsy, żeby akurat trafić w położenie y=0
    if y_nowe < 0:
        y_nowe = 0
        dt_hop = -y_stare / vy_stare  # liczenie czasu dt, po którym nastąpi odbicie od podłogi
        vy_nowe = -(vy_stare + g * dt_hop)
        x_nowe = x_stare + vx_stare * dt_hop
        t += dt_hop
    else:
        t += dt

    return x_nowe, y_nowe, vx_nowe, vy_nowe, t


def main():
    print("Symulator rzutu poziomego")
    v0 = 2 #input("Podaj prędkość początkową wyrzuconej piłki:")
    kat = 60 #input("Podaj kąt rzucenia piłki:")
    h0 = 0 #input("Podaj wysokość początkową piłki:")
    dt = 0.1 #input("Podaj czas, po którym wartości mają być aktualizowane: ")
    pilka = Pilka(v0, h0, kat)


    t = 0
    tmax = 10
    t_list, y_list =[], []

    while t <= tmax:
        #print(pilka.x, pilka.y, pilka.vx, pilka.vy)
        pilka.x, pilka.y, pilka.vx, pilka.vy, t = aktualizuj_pilke(pilka.x, pilka.y, pilka.vx, pilka.vy, t, dt)
        t_list.append(t)
        y_list.append(pilka.y)

    # wykres wysokości od czasu
    fig, ax = plt.subplots()
    ax.plot(t_list, y_list)
    plt.show()



if __name__ == "__main__":
    main()