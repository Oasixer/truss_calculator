import numpy as np
from math import sqrt as sqrt
pi = np.pi

BDy = CDy = -4.5
ADy = 9

min_cost_to_print_vals = 570

def run(H, D):
    ADx = D*ADy/H
    AD = sqrt(ADx**2 + ADy**2)
    l_BDx = D-3
    BDx = l_BDx*BDy/H
    BD = -sqrt(BDx**2 + BDy**2)
    l_CDx = (15-2*D-3)/2
    CDx = abs(l_CDx)*CDy/H
    CD = -sqrt(CDx**2 + CDy**2)
    AB = -ADx
    BC = -BDx-AB
    CC = CDx + BC
    DD = ADx + BDx - CDx

    forces = [AB, BC, AD, BD, CD, CC, DD]
    names = ['AB', 'BC', 'AD', 'BD', 'CD', 'CC', 'DD']
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
    l_DD = l_CDx * 2+3

    lengths_double = np.array([l_AB, l_BC, l_AD, l_BD, l_CD])
    lengths_single = np.array([CC, DD])

    n_joints = 8
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

    

    return cost



width_bridge = 15
width_single_pavement_member = 3

D_max = width_bridge/2-width_single_pavement_member/2 # = 4.5
D_min = 3
D_n = 10
D_array = np.linspace(D_min, D_max, num=D_n, endpoint=True)

H_min = 1
H_max = 4
H_n = 1000
H_array = np.linspace(H_min, H_max, num=H_n, endpoint=True)

#H_array = [3.404]
D_array = [3]
H_array = [3.402]

for D in D_array:
    for H in H_array:
        cost = run(H,D)
