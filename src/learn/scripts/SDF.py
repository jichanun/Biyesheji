
import matplotlib.pyplot as plt
import numpy as np

def distanceField(sp, ep):
    brx, bry = ep + np.array([25, 25])
    direct = (ep - sp).astype(np.float64)
    direct /= np.linalg.norm(direct)
    result = np.zeros((bry, brx))
    for i in range(bry):
        for j in range(brx):
            s2p = (np.array([j, i]) - sp).astype(np.float64)
            e2p = (np.array([j, i]) - ep).astype(np.float64)
            over_e = (e2p.dot(direct) >= 0)
            over_s = (s2p.dot(direct) <= 0)
            #positive = (s2p.dot(normal) > 0)
            dist = 0.0
            if (over_e == False and over_s == False):
                dist = np.sqrt(np.linalg.norm(s2p) ** 2 -(direct.dot(s2p)) ** 2)
            elif (over_e == True):
                dist = np.linalg.norm(e2p)
            else:
                dist = np.linalg.norm(s2p)
                result[i, j] = dist
    return result

def visualization(sp, ep, result):
    img = np.zeros_like(result)
    plt.imshow(result, cmap = 'inferno')
    plt.plot([sp[0], ep[0]], [sp[1], ep[1]], c = 'w')
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
        sp = np.array([25, 18])
        ep = np.array([100, 88])
        res = distanceField(sp, ep)
        visualization(sp, ep, res)