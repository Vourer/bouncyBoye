import matplotlib.pyplot as plt
import numpy as np
from math import radians, isnan

g = -9.81


class Pilka:
    # inicjalizacja obiektu piłka z zadanymi wartościami zmiennych
    def __init__(self, v0, h0, kat, m0, gamma0):
        self.vx = 0.3                       # [m/s], prędkość pozioma //np.cos(radians(kat%90)) * v0
        self.vy = np.sin(radians(kat%90)) * v0       # [m/s], prędkość pionowa
        self.x = 0                          # [m], położenie w poziomoie
        self.y = h0                         # [m], wysokość; równoznaczne z h, ale na wykresie lepsze jest y (chyba)
        self.m = m0                         # [kg], masa piłki
        self.gamma = gamma0                 # współczynnik straty energii
        self.Ek = 0.5 * self.m * self.vy ** 2   # energia kinetyczna piłki
        self.Ep = self.m * (-g) * self.y        # energia potencjalna piłki
        self.hmax = h0                      # wysokość, na jaką piłka wzbije się po odbiciu (mierzona, nie liczona)

    # funckja aktualizująca położenie i prędkość piłki stosując algorytm skokowy
    def aktualizuj_pilke(self, t, dt):
        # pierwsza część ruchu / pierwsza połowa dt
        x_pol = self.x + self.vx * 0.5 * dt
        y_pol = self.y + self.vy * 0.5 * dt

        # aktualizacja prędkości
        vx_nowe = self.vx
        vy_nowe = self.vy + g * dt

        # druga część ruchu / druga połowa dt
        x_nowe = x_pol + vx_nowe * 0.5 * dt
        y_nowe = y_pol + vy_nowe * 0.5 * dt

        # sprawdzanie czy piłka nie no-clip'uje przez podłogę
        # jeśli tak, to robimy krok czasowy trochę mniejszsy, żeby akurat trafić w położenie y=0
        if y_nowe < 0:
            y_nowe = 0
            # poniżej liczenie czasu dt, po którym nastąpi odbicie od podłogi
            dt_hop = (self.vy + np.sqrt(self.vy ** 2 + 2 * g * self.y)) / g
            if self.gamma > 0:
                vy_nowe = (-1 + self.gamma / np.sqrt(2)) * (self.vy + g * dt_hop)
            else:
                vy_nowe = -(self.vy + g * dt_hop)
            x_nowe = self.x + self.vx * dt_hop
            t += dt_hop
            odbicie = True
        else:
            t += dt
            odbicie = False

        self.x = x_nowe
        self.y = y_nowe
        self.vx = vx_nowe
        self.vy = vy_nowe
        if y_nowe > self.hmax:
            self.hmax = y_nowe

        return t, odbicie

    # funckcja zwracająca uaktualnione wartości energii potencjalnej i kinetycznej piłki
    def aktualizuj_energie(self):
        self.Ek = 0.5 * self.m * self.vy ** 2
        self.Ep = self.m * (-g) * self.y
        return self.Ek, self.Ep


def przygotuj_symulacje(v0, h0, m, gamma, tmax, dt):
    """v0 = 20     #input("Podaj prędkość początkową wyrzuconej piłki:")
    kat = 60    #input("Podaj kąt rzucenia piłki:")
    h0 = 0      #input("Podaj wysokość początkową piłki:")
    m = 5       #input("Podaj masę piłki:")
    gamma = 0.3 #input("Podaj współczynnik straty energii: //zakres <0,1>")
    tmax = 25   #input("Podaj maksymalny czas trwania symulacji:")
    dt = 0.1    #input("Podaj czas, po którym wartości mają być aktualizowane:")"""
    pilka = Pilka(v0, h0, 60, m, gamma)

    t = 0
    t_list, y_list = [0], [pilka.y]   # listy, do których po każdej iteracji będą zapisywane obecny czas i wysokość
    ek_list, ep_list = [pilka.Ek], [pilka.Ep]   # listy, do których po każdej iteracji będą zapisywane wartości energii
    e_list = [pilka.Ek + pilka.Ep]   # lista z energią całkowitą piłki, aktualizowana w każdej iteracji
    straty = []   # lista przechowująca straty energii, aktualizowana po każdym kolejnym odbiciu piłki

    while t <= tmax:
        t, odbicie = pilka.aktualizuj_pilke(t, dt)
        if isnan(t):
            break  # w pewnym momencie piłka przestaje się odbijać i 't' przyjmuje wtedy wartość 'nan' - tego nie chcemy
        if odbicie is True:
            straty.append(e_list[0] - (pilka.Ek + pilka.Ep))
        t_list.append(t)
        y_list.append(pilka.y)
        ek, ep = pilka.aktualizuj_energie()
        ek_list.append(ek)
        ep_list.append(ep)
        e_list.append(ek+ep)

    # wykres wysokości od czasu
    plt.subplot(label="wysokosc")
    plt.plot(t_list, y_list, label='wysokość [m]')
    plt.xlim(t_list[0]-dt, t_list[-1])
    plt.ylim(0, pilka.hmax+1)
    plt.title("Wykres zależności wysokości piłki h od upływu czasu t")
    plt.xlabel("t [s]")
    plt.ylabel("h [m]")
    plt.legend()
    plt.savefig('static/wysokosc.png')

    # wykres zmian energii kinetycznej i potencjalnej od czasu
    plt.subplot(label="energie")
    plt.plot(t_list, ek_list, label='Ek [J]')
    plt.plot(t_list, ep_list, label='Ep [J]')
    plt.xlim(t_list[0]-dt, t_list[-1])
    plt.ylim(0, pilka.hmax*pilka.m*g*(-1.1))
    plt.title("Wykres zależności poziomów energii piłki od upływu czasu t")
    plt.xlabel("t [s]")
    plt.ylabel("E [J]")
    plt.legend()
    plt.savefig('static/energie.png')

    # wykres zmiany energii całkowitej piłki od czasu
    plt.subplot(label="calkowita")
    plt.plot(t_list, e_list, label='Ec [J]')
    plt.xlim(t_list[0] - dt, t_list[-1])
    plt.ylim(0, e_list[0] * 1.2)
    plt.title("Wykres zależności energii całkowitej piłki od upływu czasu t")
    plt.xlabel("t [s]")
    plt.ylabel("E [J]")
    plt.legend()
    plt.savefig('static/calkowita.png')

    # wykres strat energii od liczby odbić
    plt.subplot(label="straty")
    plt.bar([x for x in range(len(straty))], straty, label='strata energii [J]')
    plt.xlim(0, len(straty))
    plt.ylim(0, e_list[0]*1.3)
    plt.title("Wykres sumy straconej energii podczas kolejnych odbić piłki")
    plt.xlabel("numer odbicia")
    plt.ylabel("E [J]")
    plt.legend()
    plt.savefig('static/straty.png')

    # zwróć całkowity czas symulacji, ilość odbić i największą osiągniętą wysokość
    return t_list[-1], len(straty), pilka.hmax


if __name__ == "__main__":
    v0 = 20  # input("Podaj prędkość początkową wyrzuconej piłki:")
    kat = 60  # input("Podaj kąt rzucenia piłki:")
    h0 = 0  # input("Podaj wysokość początkową piłki:")
    m = 5  # input("Podaj masę piłki:")
    gamma = 0.3  # input("Podaj współczynnik straty energii: //zakres <0,1>")
    tmax = 25  # input("Podaj maksymalny czas trwania symulacji:")
    dt = 0.1  # input("Podaj czas, po którym wartości mają być aktualizowane:")
    przygotuj_symulacje(v0, h0, m, gamma, tmax, dt)