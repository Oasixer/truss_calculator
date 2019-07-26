import numpy as np
from math import sqrt
import tqdm

pi = np.pi
min_cost_to_print_vals = 506
vars_ = [0,0,0]

# There are 3 inputs: h1, h2, and d

# Loose Restrictions: 1 <= h1 < 10
#                     1 <  h2 < 10
#                    -3 <= d <= 3

# Secondary Restrictions (derived):
# h1 / l_BD >= 0.5
# h1 / l_AD >= 9/12

def run(h1, h2, d, min_cost):
    # CALCULATE LENGTHS AND ANGLES------------------------------------------
    if 3 + d == 0:
        th1 = pi
    else:
        th1 = np.arctan(h1/(3+d))
    alpha4 = np.arctan(d/h1)
    th2 = pi/2 - alpha4
    th4 = np.arctan(h2/1.5)

    l_ADx = 3 + d
    l_ADy = h1

    
    l_AD = sqrt(l_ADx**2 + l_ADy**2)

    if h1/l_AD < 9/12: # see restrictions above
        # optionally print
        return

    l_BDx = abs(l_ADx-3)
    l_BDy = l_ADy
    l_CDy = l_ADy
    l_BD = sqrt(l_BDx**2 + l_BDy**2)

    if h1/l_BD < 0.5: # see restrictions above
        # optionally print
        return

    l_CDx = 6 - l_ADx
    l_CD = sqrt(l_CDx**2 + l_CDy**2)
    l_DEx = 15/2 - l_ADx
    dh = h1 - h2 # signed version of l_DEy
    l_DEy = abs(dh)

    th3 = np.arctan(dh/l_DEx)

    l_DE = sqrt(l_DEx**2 + l_DEy**2)

    l_CEx = 1.5
    l_CEy = h2
    l_CE = sqrt(l_CEx**2 + l_CEy**2)

    # FINISHED CALCULATING LENGTHS AND ANGLES------------------------------

    sin1 = np.sin(th1)
    cos1 = np.cos(th1)
    sin2 = np.sin(th2)
    cos2 = np.cos(th2)
    sin3 = np.sin(th3)
    cos3 = np.cos(th3)
    sin4 = np.sin(th4)
    cos4 = np.cos(th4)

    DE = 40.5 / ((l_ADx-6)*sin3 + h1 * cos3)
    CE = DE * (sin3/sin4)
    CC = -DE*cos3 - CE*cos4
    BD = -4.5/sin2
    if th1 == pi:
        AD = 9
    AD = 9/sin1
    AB = -AD*cos1
    BC = -AD*cos1 - BD*cos2
    CDy = -(CE*sin4 + 4.5)
    CDx = CC + CE*cos4 - BC
    if (CDx >= 0 and CDy >=0):
        CD = sqrt(CDx**2 + CDy**2)
    elif (CDx < 0 and CDy < 0):
        CD = -sqrt(CDx**2 + CDy**2)
    else:
        #print(CDx)
        #print(CDy)
        #print("HEY WHAT THE FUCK JUST HAPPENED BRO NOT COOL (ERRORRRRRRRRRR)")
        return
        #return

    forces = [AB, BC, AD, BD, CD, CC, CE, DE]
    names = ['AB', 'BC', 'AD', 'BD', 'CD', 'CC', 'CE', 'DE']
    fail = False
    for f in forces:
        #print(f)
        if f > 12 or f < -9:
            fail = True
            return

    l_AB = l_BC = l_CC = 3
    #print(fail)


    lengths_double = np.array([l_AB, l_BC, l_AD, l_BD, l_CD, l_DE, l_CE])
    lengths = [l_AB, l_BC, l_AD, l_BD, l_CD, l_DE, l_CE, l_CC]
    l_names = ['l_AB', 'l_BC', 'l_AD', 'l_BD', 'l_CD', 'l_DE', 'l_CE', 'l_CC']
    lengths_single = np.array([CC])
    n_joints = 9
    cost_per_joint = 5
    cost_per_m = 10

    cost = n_joints * cost_per_joint + cost_per_m * (2*np.sum(lengths_double) + np.sum(lengths_single)) 
    #print(cost)
    #print(cost)

    #print(f'pass, cost {cost:.2f}, h1 {h1:.3f} h2 {h2:.3f} d {d:.3f}')
    #print(f', FORCES:', end='')
    #for force, name in zip(forces, names):
    #     print(f' {name} {force:.4f}', end='')
    #for l, name in zip(lengths, l_names):
    #    print(f'{name}, {l}')
    #print(l_ADx)
    #print(l_ADy)
    #print()

    if not fail:
        if not min_cost:
            vars_[0] = h1
            vars_[1] = h2
            vars_[2] = d
        elif cost < min_cost:

            #print(f'pass, cost {cost:.2f}, h1 {h1:.3f} h2 {h2:.3f} d {d:.3f}')
            #print(f', FORCES:', end='')
            #for force, name in zip(forces, names):
            #     print(f' {name} {force:.4f}', end='')
            #for l, name in zip(lengths, l_names):
            #    print(f'{name}, {l}')
            #print(l_ADx)
            #print(l_ADy)
            #print()
            vars_[0] = h1
            vars_[1] = h2
            vars_[2] = d
        '''
    else:
        #print('fail: ', end='')
        #print(f'FORCES:', end='')
        #for force, name in zip(forces, names):
        #     print(
        pass
    '''

    return cost





h1_max = 6
h1_min = 1.2
h1_n = 10000
h1_array = np.linspace(h1_min, h1_max, h1_n, endpoint=False)

h2_max = 6
h2_min = 1.2
h2_n = 10000
h2_array = np.linspace(h2_min, h2_max, h2_n, endpoint=False)

d_max = 2.9
d_min = -2.7
d_n = 10000
d_array = np.linspace(d_min, d_max, d_n, endpoint=True)

h1_array = [2.784]
h1_n=1

#h2_array = [4.752]
#d_array = [-0.551]

n_total = h1_n * h2_n * d_n

np.random.shuffle(h1_array)
np.random.shuffle(h2_array)
np.random.shuffle(d_array)

t = tqdm.tqdm(total=n_total, dynamic_ncols=True, leave=True,
              bar_format='{l_bar}{bar}|[Elapsed: {elapsed}][Remaining: {remaining}][{rate_fmt}{postfix}]')

min_cost = None

for h1 in h1_array:
    for h2 in h2_array:
        for d in d_array:
            cost = run(h1, h2, d, min_cost)
            #print(cost)
            t.update()
            if not min_cost:
                min_cost = cost
            elif cost:
                if cost < min_cost:
                    min_cost = cost
                    #print('hi')
                    t.set_postfix({'min_cost':str(min_cost), 'h1,h2,d':vars_})

#print(f'DONE\nmin_cost ')


           
    


