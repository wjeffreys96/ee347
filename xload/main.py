import csv
import math
from dataclasses import dataclass

TOLERANCE = 1
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
    motor_loads: list[MotorSample | None] = [MotorSample(*data) for data in MOTOR_DATA]
    motor_loads.append(None)
    overload_conditions: list[OverloadCondition] = []
    calc_counter = 0

    for r in R_LOADS_OHM:
        for c in C_LOADS_OHM:
            for m in motor_loads:
                ri = wye_i_ll_from_z(r)
                ci = delta_i_ll_from_z(c)
                rs = s_from_i_ll(ri)
                cs = s_from_i_ll(ci)
                ms = m.s if m is not None else 0
                s_total = rs + cs + ms
                if abs(s_total) > OVERLOAD_LIMIT:
                    overload_conditions.append(
                        OverloadCondition(
                            abs(s_total), r, c, ms, m.nm if m is not None else None
                        )
                    )
                calc_counter += 1

    csvname = "overloads.csv"
    with open(csvname, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(
            [
                "Total S (VA)",
                "Resistive Bank Value (ohms)",
                "Capacitive Bank Value (ohms)",
                "Motor S Value (VA)",
                "Motor Torque (Nm)",
            ]
        )
        for cond in overload_conditions:
            writer.writerow(cond.to_csv_row())

    for cond in overload_conditions:
        print(cond.to_fmt_str())

    print(
        f"{'-' * 50}\nTotal found: {len(overload_conditions)}. Total Calculations: {calc_counter}"
    )

    print(f"Created CSV: '{csvname}'")


def delta_i_ll_from_z(z: complex | None) -> complex:
    """Return the line current in a delta connected load given an impedance"""
    return math.sqrt(3) * LL_VOLT_V / z if z is not None else 0


def wye_i_ll_from_z(z: complex | None) -> complex:
    """Return the line current in a wye connected load given an impedance"""
    return PHASE_VOLT_V / z if z is not None else 0


def s_from_i_ll(i_ll: complex) -> complex:
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
    m_s: complex | None
    m_nm: float | None

    def to_fmt_str(self) -> str:
        return f"s: {round(self.s_total, 2)}, r: {self.r} c: {self.c}, ms: {self.m_s}, m_torque: {self.m_nm}"

    def to_csv_row(self) -> list[float | complex | None]:
        return [round(self.s_total, 2), self.r, self.c, self.m_s, self.m_nm]


if __name__ == "__main__":
    main()
