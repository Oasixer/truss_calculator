import numpy as np
import tqdm
from math import sqrt

pi = np.pi


def run_based_on_force(CE):
    # CONSTRAINTS ---------------------------
    AD = 12
    #DE = 12
    BC = -9
    CC = -9
    #CE = -7
    #----------------------------------------

    # everything below here is derived until we get to th4 which we can't derive

    th1 = np.arcsin(9 / AD)
    sin1 = np.sin(th1)
    cos1 = np.cos(th1)
    AB = -12 * cos1  # Should = -7.937253933
    BDx = -(AB + 9)  # Should = -1.062746
    BDy = -4.5  # equal to downward weight force
    BD = -sqrt(BDx**2 + BDy**2)  # should = -4.623789485

    # Note a1 means alpha 1, a2 means alpha 2, etc. even though not every alpha variable is used here.
    a1 = np.arctan(BDy / BDx)  # should be 1.338879872
    th2 = pi - a1
    sin2 = np.sin(th2)
    cos2 = np.cos(th2)
    a2 = pi - a1 - th1  # should be 0.95465
    lBD = 3 * sin1 / np.sin(a2)  # should be 2.7569
    lAD = np.sin(a1) * lBD / sin1
    lADy = lAD * sin1  # lADy will be usefull later
    lADx = lAD * cos1  # lADx will be usefull later

    lBD = 3 * sin1 / np.sin(a2)
    lCD = sqrt(lBD**2 + 3**2 - 2 * 6 * cos2)  # by cosine law

    th3 = np.arcsin(lBD * sin2 / lCD)
    sin3 = np.sin(th3)
    cos3 = np.cos(th3)

    # At this point, we have derived AB, BD, lBD, lCD, th2, th3, a1, a2
    # But we need to choose a value of th4 or loop through values for th4.

    # th4 is important because of the following equation:
    # CD = CE * cos(th4) / cos(th3)
    # this means that the higher the value of th4 is, the higher the force on CD is

    # We are gonna loop through th4 values

    def run_based_on_th4(th4):
        print_info = True
        fail = False
        sin4 = np.sin(th4)
        cos4 = np.cos(th4)
        if print_info:
            print(f'run th4={th4} ', end='')
        CD = CE * cos4 / cos3
        #CD = (-4.5 - CE * sin4) / sin3

        if CD < -9:
            if print_info:
                print(f'CD={CD:.5f} (too much force) ', end='')
            fail = True
        else:
            if print_info:
                print(f'CD={CD:.5f} ', end='')

        CDx = CD * cos3
        CEx = CE * cos4
        print(f'Pls be zero CEx - CDx {CEx - CDx}')
        print(f'Pls be zero CD - CE * cos4 / cos3 {CD - CE * cos4 / cos3}')

        ADx = -AB
        # BDx was calculated when we calculated BD
        DEx = ADx - BDx - CDx  # cool, now we have a value for DEx
        CEy = CE * sin4
        DEy = -CEy
        DE = sqrt(DEx**2 + DEy**2)
        if DE > 12:
            if print_info:
                print(f'DE={DE:.5f} (too much force) ', end='')
            fail = True
        else:
            if print_info:
                print(f'DE={DE:.5f} ', end='')

        a6 = pi / 2 - th4  # Sorry we skipped a lot of alpha variables, we didn't end up using most of them
        lCE = 1.5 / np.sin(a6)
        lCEy = lCE * sin4  # I called lCEy  h on paper for some dumb reason
        lDEy = lCEy - lADy

        lAEx = 7.5
        lDEx = lAEx - lADx
        lDE = sqrt(lDEx**2 + lDEy**2)

        # We have now assumed or derived values for everything! We can calculate cost:
        lengths = [lBD, lAD, lCD, lCE, lDE]
        n_joints = 9
        meters_pavement = 15
        pavement_cost = meters_pavement * 10
        cost__ = n_joints * 5 + pavement_cost

        for length in lengths:
            cost__ += 20 * length
            if length < 1:
                print(f'FUCK this shit im out. Length={length}, cannot be <1 nerd')
                return

        other_members = [AD, AB, BD, BC, CE, CC]
        names = ['AD', 'AB', 'BD', 'BC', 'CD', 'CC']

        # print('FORCES:\n')
        for member, name in zip(other_members, names):
            if member > 12 or member < -9:
                print(f'{name} {member} too much force', end='')
                fail = True

        if print_info:
            print(f'cost {cost__}')
        #print(fail, end='')

        return cost__ if not fail else None

    min_cost_ = None
    for th4 in th4_array:
        cost_ = run_based_on_th4(th4)
        if cost_:
            if not min_cost_:
                min_cost_ = cost_
            elif cost_ < min_cost_:
                min_cost_ = cost_

    return min_cost_

    '''
    # 0 = DEx + BDx + CDx - ADx

    print(ADx)
    print(BDx)
    print(CDx)
    print(f'DEx = {DEx}')
    # Let's check this value against DE=12 using triangle ratio
    DEx_v2 = DE * (lDEx / lDE)

    # and hope to god these values subtract to zero
    print(f'PLEASE BE ZERO {DEx - DEx_v2}')
    '''


min_cost = None
th4_n = 50
th4_min = 0.2
th4_max = pi / 2 - 0.01
global th4_array
th4_array = np.linspace(th4_min, th4_max, num=th4_n, endpoint=False)

CE_min = -4
CE_max = -9
CE_n = 10
CE_array = np.linspace(CE_min, CE_max, num=CE_n, endpoint=True)

for ce in CE_array:
    cost = run_based_on_force(ce)
    if not min_cost:
        min_cost = cost
    elif cost:
        if cost < min_cost:
            min_cost = cost
    print(f'run CE={ce} cost={cost}\n')
print(f'Done all. min_cost = {min_cost}')


'''
n_each = 95
n = n_each ** 4
minim = 0.3

min_cost = 100000000

print(f'running {n} iterations')

# new constraints
th4_min = 0.45
th4_max = 1

th5_min = 0.25
th5_max = 0.7  # usuallymin of this and th4

th3_min = 0.1
th3_max = 1  # usually 0.6

th2_min = 1
th2_max = 2

th1 = []

#th3 = [0.45]
#th5 = [0.45]
i = 0
th4 = np.linspace(th4_min, th4_max, num=n_each, endpoint=False)
#th4 = [0.85]
t = tqdm.tqdm(total=n, dynamic_ncols=True, leave=False,
              bar_format='{l_bar}{bar}|[Elapsed: {elapsed}][Remaining: {remaining}][Samples: {n_fmt}/{total_fmt}][{rate_fmt}{postfix}]')
for th4_ in th4:
    th5 = np.linspace(th5_min, th5_max, num=n_each, endpoint=False)  # min(th4_, th5_max), num=n_each, endpoint=False)
    #th5 = [1]
    th3 = np.linspace(th3_min, min(th3_max, pi - th4_), num=n_each, endpoint=False)
    #th3 = [0.635]
    # print(th3)
    for th3_ in th3:
        #th2 = [1.8]
        th2 = np.linspace(th2_min, min(th2_max, pi - th3_), num=n_each, endpoint=False)
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
print(f'th5 min {np.min(th5s)} max {np.max(th5s)} best {th5_best[-1]}')'''
