import matplotlib.pyplot as plt
import numpy as np
from math import radians, isnan

g = -9.81


class Pilka:
    # na razie "działa" część od rzutu pionowego
    # może niedługo  piłka będzie się poruszać w dwóch wymiarach, pod zadanym kątem początkowym
    # inicjalizacja obiektu piłka z zadanymi wartościami zmiennych
    def __init__(self, v0, h0, kat, m0, gamma0):
        self.vx = 0.3                       # [m/s], prędkość pozioma //np.cos(radians(kat%90)) * v0
        self.vy = np.sin(radians(kat%90)) * v0       # [m/s], prędkość pionowa
        self.x = 0                          # [m], położenie w poziomoie
        self.y = h0                         # [m], wysokość; równoznaczne z h, ale na wykresie lepsze jest y (chyba)
        self.m = m0                         # [kg], masa piłki
        self.gamma = gamma0
        self.Ek = 0.5 * self.m * self.vy ** 2
        self.Ep = self.m * (-g) * self.y
    
    # funckcja zwracająca uaktualnione wartości energii potencjalnej i kinetycznej piłki
    def aktualizuj_energie(self):
        self.Ek = 0.5 * self.m * self.vy ** 2
        self.Ep = self.m * (-g) * self.y
        return self.Ek, self.Ep
    
    # funkcja zwracająca różnicę poprzednio odnotowanej Ek i nowej, obliczonej ze zmienioną po odbiciu prędkością piłki
    def policz_strate(self):
        return self.Ek - (0.5 * self.m * self.vy ** 2)


def aktualizuj_pilke(x_stare, y_stare, vx_stare, vy_stare, gamma, t, dt):
    # uaktualnienie położenia x i y oraz prędkości vy stosując algorytm skokowy
    # pierwsza część ruchu / pierwsza połowa dt
    x_pol = x_stare + vx_stare * 0.5*dt
    y_pol = y_stare + vy_stare * 0.5*dt

    # aktualizacja prędkości
    vx_nowe = vx_stare
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
        if gamma > 0:
            vy_nowe = (-1 + gamma)*(vy_stare + g * dt_hop)
        else:
            vy_nowe = -(vy_stare + g * dt_hop)
        x_nowe = x_stare + vx_stare * dt_hop
        t += dt_hop
        odbicie = True
    else:
        t += dt
        odbicie = False

    return x_nowe, y_nowe, vx_nowe, vy_nowe, t, odbicie


def main():
    v0 = 20     #input("Podaj prędkość początkową wyrzuconej piłki:")
    kat = 60    #input("Podaj kąt rzucenia piłki:")
    h0 = 0      #input("Podaj wysokość początkową piłki:")
    m = 5       #input("Podaj masę piłki:")
    dt = 0.1    #input("Podaj czas, po którym wartości mają być aktualizowane:")
    tmax = 15   #input("Podaj maksymalny czas trwania symulacji:")
    gamma = 0.3 #input("Podaj współczynnik straty energii: //zakres <0,1>")
    pilka = Pilka(v0, h0, kat, m, gamma)

    t = 0
    t_list, y_list = [0], [pilka.y]   # listy, do których po każdej iteracji będą zapisywane obecny czas i wysokość
    ek_list, ep_list = [pilka.Ek], [pilka.Ep]   # listy, do których po każdej iteracji będą zapisywane wartości energii
    straty = []   # lista zawierająca straty energii, aktualizowana po każdym kolejnym odbiciu piłki

    while t <= tmax:
        pilka.x, pilka.y, pilka.vx, pilka.vy, t, odbicie = aktualizuj_pilke(pilka.x, pilka.y, pilka.vx, pilka.vy, pilka.gamma, t, dt)
        if isnan(t):
            break  # w pewnym momencie piłka przestaje się odbijać i 't' przyjmuje wtedy wartość 'nan' - tego nie chcemy
        if odbicie is True:
            straty.append(pilka.policz_strate())
        t_list.append(t)
        y_list.append(pilka.y)
        ek, ep = pilka.aktualizuj_energie()
        ek_list.append(ek)
        ep_list.append(ep)

    # wykres wysokości od czasu
    plt.subplot(3, 1, 1)
    plt.plot(t_list, y_list, label='wysokość [m]')
    plt.xlim(t_list[0]-dt, t_list[-1])
    plt.ylim(bottom = 0)
    plt.title("Wykres zależności wysokości piłki h od upływu czasu t")
    plt.xlabel("t [s]")
    plt.ylabel("h [m]")
    plt.legend()

    # wykres zmian energii od czasu
    plt.subplot(3, 1, 2)
    plt.plot(t_list, ek_list, label='Ek [J]')
    plt.plot(t_list, ep_list, label='Ep [J]')
    plt.xlim(t_list[0]-dt, t_list[-1])
    plt.ylim(0, ek_list[0]*1.2)
    plt.title("Wykres zależności poziomów energii piłki od upływu czasu t")
    plt.xlabel("t [s]")
    plt.ylabel("E [J]")
    plt.legend()

    # wykres strat energii od liczby odbić
    plt.subplot(3, 1, 3)
    plt.plot([x+1 for x in range(len(straty))], straty, label='strata energii [J]')
    plt.xlim(0, len(straty))
    plt.ylim(0, ek_list[0])
    plt.title("Wykres ilości straconej energii podczas kolejnych odbić piłki")
    plt.xlabel("numer odbicia")
    plt.ylabel("E [J]")
    plt.legend()
    plt.show()
    
    return


if __name__ == "__main__":
    main()
