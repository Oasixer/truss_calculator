import numpy as np
import tqdm

pi = np.pi

th2s = [12345]
th3s = [12345]
th4s = [12345]
th5s = [12345]
th2_best = [12345]
th3_best = [12345]
th4_best = [12345]
th5_best = [12345]


def run(th1, th2, th3, th4, th5, min_cost, debug=False):
    sin1 = np.sin(th1)
    cos1 = np.cos(th1)

    sin2 = np.sin(th2)
    cos2 = np.cos(th2)

    sin3 = np.sin(th3)
    cos3 = np.cos(th3)

    sin4 = np.sin(th4)
    cos4 = np.cos(th4)

    sin5 = np.sin(th5)
    cos5 = np.cos(th5)

    cos2m1 = np.cos(th2 - th1)
    sin4m5 = np.sin(th4 - th5)
    cos4m5 = np.cos(th4 - th5)

    l_BD = 3 * sin1 / (np.sin(th2 - th1))
    if l_BD < 1:
        return 100000
    l_AD = l_BD * np.sin(pi - th2) / sin1
    if l_AD < 1:
        return 100000
    l_CD = 3 * sin2 / np.sin(pi - th2 - th3)
    if l_CD < 1:
        return 100000
    l_CE = 3 * sin4 / np.sin(pi - 2 * th4)
    if l_CE < 1:
        return 100000
    l_DE = np.sin(pi - th3 - th4) * l_CD / sin5
    if l_DE < 1:
        return 100000

    lengths = [l_BD, l_AD, l_CD, l_CE, l_DE]

    # for name, length in zip(l_names, lengths):
    #   if length < 1:
    # print(f'ERROR! {name} < 0, = {length}')
    #       return False
    print('hi')

    AD = 9 / sin1
    if AD < -9 or AD > 12:
        return 100000
    AB = -AD * cos1
    if AB < -9 or AB > 12:
        return 100000
    BD = -4.5 / sin2
    if BD < -9 or BD > 12:
        return 100000
    #print('hi2')
    BC = AB - BD * cos2
    if BC < -9 or BC > 12:
        return 100000
    #print('hi3')
    DE = (4.5 * cos3 / sin3 + BD * cos2 + AD * cos2m1) / (sin4m5 * cos3 / sin3 + cos4m5)
    if DE < -9 or DE > 12:
        return 100000
    #print('hi4')
    CE = -DE * sin4m5 / sin4
    if CE < -9 or CE > 12:
        return 100000
    #print('hi5')
    CD = (-4.5 - DE * sin4m5) / sin3
    if CD < -9 or CD > 12:
        return 100000
    CC = BC - CE * cos4 + CD * cos3
    if CC < -9 or CC > 12:
        return 100000

    '''for member, name in zip(members, names):
        if debug:
            print(f'{name} : {member}')

        if member < -9:
            if debug:
                print(f'compress fail {name} {member}')
            return

        if member > 12:
            if debug:
                print(f'tension fail {name} {member}')
            return'''

    n_joints = 9
    meters_pavement = 15
    pavement_cost = meters_pavement * 10
    cost = n_joints * 5 + pavement_cost

    for length in lengths:
        cost += 20 * length

    if cost > 600:
        return cost

    '''for name, length in zip(l_names, lengths):
        if length < 0:
            print(f'ERROR! {name} < 0, = {length}')
        cost += 10 * length * 2'''

    # print(cost)
    print('hi2')

    members = [AD, AB, BD, BC, DE, CE, CD, CC]
    names = ['AD', 'AB', 'BD', 'BC', 'DE', 'CE', 'CD', 'CC']
    l_names = ['l_BD', 'l_AD', 'l_CD', 'l_CE', 'l_DE']

    if(cost < 620):
        th2s.append(th2)
        th3s.append(th3)
        th4s.append(th4)
        th5s.append(th5)
        if cost < min_cost:
            print(f'\nJUST HIT {cost} SO, LOW COST ANALYSIS THING:\n')
            print(f'ANGLES: th1 {th1} th2 {th2} th3 {th3} th4 {th4} th5 {th5} \n\nLENGTHS:')
            for name, length in zip(l_names, lengths):
                print(f'{name} = {length}')
            print('\nFORCES:\n')
            for member, name in zip(members, names):
                print(f'{name} : {member}')
            print('\n')
            th2_best.append(th2)
            th3_best.append(th3)
            th4_best.append(th4)
            th5_best.append(th5)

    return cost


n_each = 80
n = n_each ** 4
minim = 0.3

min_cost = 100000000

print(f'running {n} iterations')

# new constraints
th4_min = 0.01
th4_max = 1.25

th5_min = 0.01
th5_max = 1.25  # usuallymin of this and th4

th3_min = 0.01
th3_max = 1  # usually 0.6

th2_min = 1.4
th2_max = 2

th1 = [np.arcsin(9 / 12)]

#th3 = [0.45]
#th5 = [0.45]
i = 0
#th4 = np.linspace(th4_min, th4_max, num=n_each, endpoint=False)
th4 = [0.85]
t = tqdm.tqdm(total=n, dynamic_ncols=True, leave=False,
              bar_format='{l_bar}{bar}|[Elapsed: {elapsed}][Remaining: {remaining}][Samples: {n_fmt}/{total_fmt}][{rate_fmt}{postfix}]')
for th4_ in th4:
    # th5 = np.linspace(th5_min, th5_max, num=n_each, endpoint=False)  # min(th4_, th5_max), num=n_each, endpoint=False)
    th5 = [1]
    #th3 = np.linspace(th3_min, min(th3_max, pi - th4_), num=n_each, endpoint=False)
    th3 = [0.635]
    # print(th3)
    for th3_ in th3:
        th2 = [1.8]
        #th2 = np.linspace(th2_min, min(th2_max, pi - th3_), num=n_each, endpoint=False)
        for th2_ in th2:
            # th1_ constrained to 1 value above
            for th1_ in th1:
                for th5_ in th5:
                    #th5_ = th4_
                    cost = run(th1_, th2_, th3_, th4_, th5_, min_cost)
                    if (i % 5000 == 0 or cost < min_cost):
                        print(
                            f'run th1 {th1_:.6f} th2 {th2_:.6f} th3 {th3_:.6f} th4 {th4_:.6f} th5 {th5_:.6f} cost {cost:2f} {"MIN" if cost < min_cost else ""}')
                        if cost < min_cost:
                            min_cost = cost

                        i += 1
                    t.update()


print(f'DONE! min={min_cost}')
th2s = np.array(th2s)
th3s = np.array(th3s)
th4s = np.array(th4s)
th5s = np.array(th5s)
print(f'th2 min {np.min(th2s)} max {np.max(th2s)} best {th2_best[-1]}')
print(f'th3 min {np.min(th3s)} max {np.max(th3s)} best {th3_best[-1]}')
print(f'th4 min {np.min(th4s)} max {np.max(th4s)} best {th4_best[-1]}')
print(f'th5 min {np.min(th5s)} max {np.max(th5s)} best {th5_best[-1]}')
