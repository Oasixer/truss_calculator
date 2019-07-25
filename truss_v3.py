import numpy as np
from math import sqrt as sqrt

BDy = CDy = -4.5
ADy = 9


def run(H, D=3):
    D=3
    ADx = D*ADy/H
    AD = sqrt(ADx**2 + ADy**2)
    # assuming D=3
    BD = -4.5
    AB=-ADx
    BC=AB

    th1 = np.arctan(H/D)
    th2 = np.arctan(H/1.5)
    CE = 4.5/np.sin(th2)
    DE = (6*CE*np.sin(th2)+4.5)/H
    CC = -DE -CE * np.cos(th2)
    CD = (BC + DE)/np.cos(th1)

    forces = [AB, BC, AD, BD, CD, CC, CE, DE]
    names = ['AB', 'BC', 'AD', 'BD', 'CD', 'CC', 'CE', 'DE']
    fail = False
    for f in forces:
        #print(f)
        if f > 12 or f < -9:
            fail = True

    l_AB = l_BC = l_CC = 3
    l_ADx = D
    l_ADy = H
    l_AD = sqrt(l_ADx**2 + l_ADy**2)
    l_BDx = D-3
    l_BDy = H
    l_BD = sqrt(l_BDx**2 + l_BDy**2)
    l_CDx = (15-2*D-3)/2
    l_CDy = H
    l_CD = sqrt(l_CDx**2 + l_CDy**2)
    l_CEx = 1.5
    l_CEy = H
    l_CE = sqrt(l_CEx**2 + l_CEy**2)
    l_DE = 15/2-D

    lengths_double = np.array([l_AB, l_BC, l_AD, l_BD, l_CD, l_DE, l_CE])
    lengths_single = np.array([CC])
    n_joints = 9
    cost_per_joint = 5
    cost_per_m = 10

    cost = n_joints * cost_per_joint + cost_per_m * (2*np.sum(lengths_double) + np.sum(lengths_single)) 

    if not fail:
        print(f'pass, cost {cost:.2f}, H {H:.3f} D {D:.3f}')
        if cost < min_cost_to_print_vals:
            print(f'FORCES:', end='')
            for force, name in zip(forces, names):
                 print(f' {name} {force:.4f}', end='')
            print()
    else:
        print('fail:')
        print(f'FORCES:', end='')
        for force, name in zip(forces, names):
             print(f' {name} {force:.4f}', end='')
        print()

    

    return cost

H_min = 1
H_max = 5
H_n = 10
H_array = np.linspace(H_min, H_max, num=H_n, endpoint=True)

#H_array = [3.404]
D_array = [3]
H_array = [3.402]

for D in D_array:
    for H in H_array:
        cost = run(H,D)
