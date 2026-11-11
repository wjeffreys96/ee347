from dataclasses import dataclass

# v, i, p, q
MOT_DAT = [
    (225.8, 0.689, 107.2, 218.9),
    (228.7, 0.748, 109.9, 147.4),
    (227.9, 0.784, 136.6, 155.9),
    (225.1, 0.845, 169.9, 168.0),
    (224.3, 0.900, 208.4, 175.5),
    (224.4, 0.954, 222.1, 187.3),
    (223.8, 1.027, 264.1, 194.6),
    (224.0, 1.108, 293.4, 207.7),
    (222.6, 1.193, 327.0, 218.4),
]

OVERLOAD_LIMIT = 3 * 250
SYS_VOLT_V = 208
R_LOADS_OHM = [0, 200, 240, 300, 400, 600, 1200]
C_LOADS_OHM = [0, -200j, -240j, -300j, -400j, -600j, -1200j]


def wye_bank_s(r: float) -> complex:
    if r == 0:
        return 0j
    return SYS_VOLT_V**2 / r


def delta_bank_s(x: complex) -> complex:
    if x == 0j:
        return x
    return 3 * (SYS_VOLT_V**2 / x.conjugate())


@dataclass()
class MotorLoad:
    v: float
    i: float
    p: float
    q: float

    @property
    def s(self) -> complex:
        return complex(self.p, self.q)


def main() -> None:
    motor_loads = [MotorLoad(*data) for data in MOT_DAT]

    for r in R_LOADS_OHM:
        for c in C_LOADS_OHM:
            for m in motor_loads:
                s = wye_bank_s(r) + delta_bank_s(c) + m.s
                if abs(s) > OVERLOAD_LIMIT:
                    print(abs(s), r, c, m.s)


if __name__ == "__main__":
    main()
