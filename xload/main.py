import math
from dataclasses import dataclass
from typing import override

TOLERANCE = 0.95
XFMR_S_RATING_VA = 250
NUM_XFMR = 3
PHASE_VOLT_V = 120
LL_VOLT_V = PHASE_VOLT_V * math.sqrt(3)
OVERLOAD_LIMIT = NUM_XFMR * XFMR_S_RATING_VA * TOLERANCE

# rpm, nm, v, i, p, q, hz
MOTOR_DATA = [
    (1770, 0, 225.8, 0.689, 107.2, 218.9, 60),
    (1766, 0.362, 228.7, 0.748, 109.9, 147.4, 60),
    (1753, 0.513, 227.9, 0.784, 136.6, 155.9, 60),
    (1739, 0.659, 225.1, 0.845, 169.9, 168, 60),
    (1728, 0.779, 224.3, 0.9, 208.4, 175.5, 60),
    (1718, 0.864, 224.4, 0.954, 222.1, 187.3, 60),
    (1703, 1.023, 223.8, 1.027, 264.1, 194.6, 60),
    (1688, 1.144, 224, 1.108, 293.4, 207.7, 60),
    (1672, 1.262, 222.6, 1.193, 327, 218.4, 60),
]

R_LOADS_OHM = [None, 171.4, 200, 240, 300, 400, 600, 1200]
C_LOADS_OHM = [None, -171.4j, -200j, -240j, -300j, -400j, -600j, -1200j]


def main() -> None:
    motor_loads = [MotorSample(*data) for data in MOTOR_DATA]
    overload_conditions: list[OverloadCondition] = []

    for r in R_LOADS_OHM:
        for c in C_LOADS_OHM:
            for m in motor_loads:
                ri = wye_i_from_z(r)
                ci = delta_i_from_z(c)
                rs = s_from_i(ri)
                cs = s_from_i(ci)
                ms = m.s
                s_total = rs + cs + ms
                if abs(s_total) > OVERLOAD_LIMIT:
                    overload_conditions.append(
                        OverloadCondition(abs(s_total), r, c, m.s)
                    )

    for cond in overload_conditions:
        print(cond)

    print(f"Total found: {len(overload_conditions)}")


def delta_i_from_z(z: complex | None) -> complex:
    """Return the current in a delta connected load given an impedance"""
    return math.sqrt(3) * LL_VOLT_V / z if z is not None else 0


def wye_i_from_z(z: complex | None) -> complex:
    """Return the current in a wye connected load given an impedance"""
    return PHASE_VOLT_V / z if z is not None else 0


def s_from_i(i_ll: complex) -> complex:
    """Calculate the total complex power in a load given the line current"""
    return math.sqrt(3) * LL_VOLT_V * i_ll.conjugate() if i_ll != 0 else 0


@dataclass()
class MotorSample:
    rpm: float
    nm: float
    v: float
    i: float
    p: float
    q: float
    hz: float

    @property
    def s(self) -> complex:
        return complex(self.p, self.q)


@dataclass()
class OverloadCondition:
    s_total: float
    r: float | None
    c: complex | None
    ms: complex

    @override
    def __repr__(self) -> str:
        return f"s: {round(self.s_total, 2)}, r: {self.r} c: {self.c}, ms: {self.ms}"


if __name__ == "__main__":
    main()
