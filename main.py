import math
import matplotlib.pyplot

r = float(input("Введите внутренний радиус r (см): ")) / 100
R = float(input("Введите внешний радиус R (см): ")) / 100
V = float(input("Введите начальную скорость V (м/с): "))
L = float(input("Введите длину конденсатора L (см): ")) / 100

e = 1.6 * 10 ** (-19)  # заряд электрона
m = 9.1 * 10 ** (-31)  # масса электрона
d = R - r  # расстояние между обкладками
toch = 1000  # точность разбиения по времени

# Бинарный поиск минимального напряжения U
left = 2  # минимальное значение U
right = 100  # максимальное значение U
while right - left > 0.00001:  # точность поиска
    mid = (left + right) / 2
    U = mid
    a_koef = e * U / (m * math.log(R / r))
    pos = d / 2  # начальное положение электрона (посередине между обкладками)
    r_cur = pos + r
    a = a_koef / r_cur
    vy = 0
    t = 0
    dt = L / (V * toch)
    escaped = True
    for _ in range(toch):
        pos = max(pos - vy * dt - a * dt ** 2 / 2, 0)
        if pos == 0:
            escaped = False
            break
        vy += a * dt
        r_cur = pos + r
        a = a_koef / r_cur
        t += dt
        if t > (L / V):
            break
    if escaped:
        left = mid
    else:
        right = mid
U_ans = right
print(f"Минимальное значение U: {U_ans:.5f} В")

# Расчет траектории электрона при минимальном U
U = U_ans
a_koef = e * U / (m * math.log(R / r))
pos = d / 2
r_cur = pos + r
a = a_koef / r_cur
vy = 0
t = 0
dt = L / (V * toch)
x_ = []
y_ = []
t_ = []
Vy = []
Ay = []
for _ in range(toch):
    t_.append(t)
    Ay.append(a)
    Vy.append(vy)
    x_.append(V * t)
    y_.append(pos)
    if pos == 0:
        break
    pos = max(pos - vy * dt - a * dt ** 2 / 2, 0)
    vy = vy if pos == 0 else vy + a * dt
    r_cur = pos + r
    a = a if pos == 0 else a_koef / r_cur
    t += dt
v_ans = math.sqrt(V ** 2 + vy ** 2)
t_ans = t
print(f"Время полета: {t_ans:.5e} с")
print(f"Конечная скорость: {v_ans:.5e} м/с")

matplotlib.pyplot.subplot(2, 2, 1)
matplotlib.pyplot.plot(x_, y_)
matplotlib.pyplot.axis((0, L, 0, R - r))
matplotlib.pyplot.title("y(x)")
matplotlib.pyplot.subplot(2, 2, 2)
matplotlib.pyplot.plot(t_, Vy)
matplotlib.pyplot.title("Vy(t)")
matplotlib.pyplot.subplot(2, 2, 3)
matplotlib.pyplot.plot(t_, Ay)
matplotlib.pyplot.title("Ay(t)")
matplotlib.pyplot.subplot(2, 2, 4)
matplotlib.pyplot.plot(t_, y_)
matplotlib.pyplot.title("y(t)")
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.show()