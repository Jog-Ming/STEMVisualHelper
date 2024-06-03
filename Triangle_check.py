from math import radians, degrees, sin, asin, cos, acos, sqrt

ZERO = 1e-5
inf = 1e10


def area(a: float, b: float, c: float) -> float:

    p = (a + b + c) / 2

    return sqrt(p * (p - a) * (p - b) * (p - c))

def tri_type(v):
    ZERO = 1e-2
    s1 = v[0]
    s2 = v[1]
    s3 = v[2]
    a1 = v[3]
    a2 = v[4]
    a3 = v[5]

    d12 = abs(s1 - s2)
    d23 = abs(s2 - s3)
    d13 = abs(s1 - s2)
    t = ""
    if d12 < ZERO and d23 < ZERO and d13 < ZERO:
        t += "equilateral "
    elif d12 < ZERO and d23 < ZERO or d12 < ZERO and d13 < ZERO or d23 < ZERO and d12 < ZERO:
        t += "isosceles "
    else:
        t += "scalene "
    if a1 > 90 or a2 > 90 or a3 > 90:
        t = "obtuse " + t
    elif abs(a1 - 90) < ZERO or abs(a1 - 90) < ZERO or abs(a1 - 90) < ZERO:
        t = "right " + t
    elif t != "equilateral ":
        t = "acute " + t
    t += "triangle"
    return t


def tri_check(s: list, a: list) -> bool:
    # Given the three sides and angles, check if the triangle exists
    # If it exists, return True; if it does not exists, return False
    
    ZERO = 1

    s1 = s[0]
    s2 = s[1]
    s3 = s[2]

    a1 = a[0]
    a2 = a[1]
    a3 = a[2]
    
    # calculate the angles using the sides
    if (s2 ** 2 + s3 ** 2 - s1 ** 2) / 2 / s2 / s3 > 1 or (s2 ** 2 + s3 ** 2 - s1 ** 2) / 2 / s2 / s3 < -1:
        return False
    if (s1 ** 2 + s3 ** 2 - s2 ** 2) / 2 / s1 / s3 > 1 or (s1 ** 2 + s3 ** 2 - s2 ** 2) / 2 / s1 / s3 < -1:
        return False
    a1_cal = degrees(acos((s2 ** 2 + s3 ** 2 - s1 ** 2) / 2 / s2 / s3))
    a2_cal = degrees(acos((s1 ** 2 + s3 ** 2 - s2 ** 2) / 2 / s1 / s3))
    a3_cal = 180 - a1 - a2

    # check if the sides are correct and the calculated angles match the given angles
    if (s1 + s2 > s3 and s2 + s3 > s1 and s3 + s1 > s2) and (abs(a1 - a1_cal) < ZERO and abs(a2 - a2_cal) < ZERO and abs(a3 - a3_cal) < ZERO):
        return True  
    else:
        print(a1, a1_cal)

        return False


def tri_solve(sides: dict, angles: dict) -> list:
    
    ZERO = 1e-5

    inf = 1e10
    side_names = ('a', 'b', 'c')

    angle_names = tuple(i.upper() for i in side_names)

    if any(i <= ZERO for i in sides.values()) or any(i <= ZERO or i >= 180 - ZERO for i in angles.values()):

        return [-1]
    if len(sides) == 0:

        # AAA
        a1 = angles['A']
        a2 = angles['B']
        a3 = angles['C']
        if abs(sum(angles.values()) - 180) < ZERO:
            s1 = 1
            s2 = sin(radians(a2)) / sin(radians(a1))
            s3 = sin(radians(a3)) / sin(radians(a1))
            return [inf, [s1, s2, s3, a1, a2, a3]]
        else:

            return [-1]
    elif len(sides) == 1:

        # AAS or ASA

        a1n, a2n = angles

        a1, a2 = dict(angles).values()

        a3n = tuple(set(angle_names) - set(angles))[0]

        a3 = 180 - a1 - a2

        angles[a3n] = a3

        if a3 <= ZERO:

            return [-1]
        else:

            tn = a3n

            t = a3

            s1n = tuple(sides)[0]

            a1n = s1n.upper()

            a2n, a3n = set(angle_names) - {a1n}

            s2n = a2n.lower()

            s3n = a3n.lower()

            s1 = sides[s1n]

            a1 = angles[a1n]

            a2 = angles[a2n]

            a3 = angles[a3n]


            s2 = s1 * sin(radians(a2)) / sin(radians(a1))

            s3 = s1 * sin(radians(a3)) / sin(radians(a1))

            return [s1, s2, s3, a1, a2, a3]
        
            # print(f"{s2n} = {round(s2,4):.3f}, {s3n} = {round(s3,4):.3f}, ∠{tn} = {round(t,4):.3f}°")

    elif len(sides) == 2:

        # SSA or SAS

        a1n = tuple(angles)[0]

        a1 = angles[a1n]

        if a1n.lower() in sides:

            # SSA

            s1n = a1n.lower()

            s2n = tuple(set(sides) - set(s1n))[0]

            s3n = tuple(set(side_names) - set(sides))[0]

            a2n = s2n.upper()

            a3n = tuple(set(angle_names) - {a1n, a2n})[0]

            s1 = sides[s1n]

            s2 = sides[s2n]

            # s1, s2, a1

            delta = s2 * sin(radians(a1)) / s1

            if (a1 == 90 and s1 == s2):
                return [-1]
            if abs(delta - 1) < ZERO or delta < 1 and (s1 > s2 or s1 == s2 and a1 < 90):

                a2 = degrees(asin(delta))

                a3 = 180 - a1 - a2

                s3 = s1 * sin(radians(a3)) / sin(radians(a1))

                return [s1, s2, s3, a1, a2, a3]
                
                # print(f"{s3n} = {round(s3,4):.3f}, ∠{a2n} = {round(a2,4):.3f}°, ∠{a3n} = {round(a3,4):.3f}°")

                
            elif delta < 1:

                if s1 == s2:

                    return[-1]
                else:

                
                    sin_a2 = s2 * sin(radians(a1)) / s1

                    a2 = degrees(asin(sin_a2))

                    a3 = 180 - a1 - a2

                    s3 = s1 * sin(radians(a3)) / sin(radians(a1))

                    

                    alter_a2 = 180 - a2

                    alter_a3 = 180 - a1 - alter_a2

                    alter_s3 = s1 * sin(radians(alter_a3)) / sin(radians(a1))

                    return [[s1, s2, s3, a1, a2, a3], [s1, s2, alter_s3, a1, alter_a2, alter_a3]]
            else:

                return[-1]
            
        else:

            s1n = tuple(set(side_names) - set(sides))[0]

            s2n, s3n = sides

            a2n = s2n.upper()

            a3n = s3n.upper()

            s2 = sides[s2n]

            s3 = sides[s3n]


            s1 = sqrt(s2 ** 2 + s3 ** 2 - 2 * s2 * s3 * cos(radians(a1)))

            a2 = degrees(acos((s1 ** 2 + s3 ** 2 - s2 ** 2) / 2 / s1 / s3))

            a3 = 180 - a1 - a2

            return [s1, s2, s3, a1, a2, a3]
            #print(f"{s1n} = {round(s1,4):.3f}, ∠{a2n} = {round(a2,4):.3f}°, ∠{a3n} = {round(a3,4):.3f}°")


    else:

        s1n, s2n, s3n = side_names

        a1n, a2n, a3n = angle_names

        s1, s2, s3 = sides.values()

        if s1 + s2 > s3 and s2 + s3 > s1 and s3 + s1 > s2:

            a1 = degrees(acos((s2 ** 2 + s3 ** 2 - s1 ** 2) / 2 / s2 / s3))

            a2 = degrees(acos((s1 ** 2 + s3 ** 2 - s2 ** 2) / 2 / s1 / s3))

            a3 = 180 - a1 - a2

            return [s1, s2, s3, a1, a2, a3]
            #print(f"∠{a1n} = {round(a1,4):.3f}°, ∠{a2n} = {round(a2,4):.3f}°, ∠{a3n} = {round(a3,4):.3f}°")

        else:

            return [-1]


def tri_n(sides: dict, angles: dict, num_data: int) -> list:
    ZERO = 0.1
    angles_name = ["A", "B", "C"]
    v = [0, 0, 0, 0, 0, 0]
    num_data -= 3

    if num_data == 0:
        tri = tri_solve(sides, angles)
        return tri

    for i in range(2, -1, -1):
        if num_data == 0:
            break
        if angles_name[i] in angles.keys():
            v[i + 3] = angles[angles_name[i]]
            del angles[angles_name[i]]
            num_data -= 1

    tri = tri_solve(sides, angles)

    if tri[0] == -1:
        return [-1]
    elif len(tri) == 2:
        for i in range(2):
            ok = False
            for j in range(6):
                if v[j] != 0:
                    if abs(v[j] - tri[i][j]) > ZERO:
                        ok = False
            if ok:
                return tri[i]
        return [-1]
    else:
        ok = True
        # print(v)
        # print(tri)
        for i in range(6):
            if v[i] != 0:
                if abs(v[i] - tri[i]) > ZERO:
                    ok = False
        if ok:
            return tri
        return [-1]

