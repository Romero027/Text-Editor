import matplotlib.pyplot as plt
import numpy as np
from numpy import *
import re, math
#import seaborn as sns
from matplotlib import rcParams
import pandas as pd
import matplotlib, csv
from matplotlib import rc
#from pyemd import emd
#import dit
#from dit.divergences import jensen_shannon_divergence
import pickle

rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)


def cdf_transfer(X):
    X = sorted(X)
    Y=[]
    l=len(X)
    Y.append(float(1)/l)
    for i in range(2,l+1):
        Y.append(float(1)/l+Y[i-2])

    return X, Y

def plot_cdf(datas, linelabels = None, label = None, y_label = "CDF", name = "ss"):
    _fontsize = 8
    fig = plt.figure(figsize=(2.5, 1.8)) # 2.5 inch for 1/3 double column width
    #fig = plt.figure(figsize=(3.7, 2.4))
    ax = fig.add_subplot(111)

    plt.ylabel(y_label, fontsize=_fontsize)
    plt.xlabel(label, fontsize=_fontsize)

    # Using seaborn color palatte "muted"
    colors = [
    #'grey',#(0.9333333333333333, 0.5215686274509804, 0.2901960784313726),
    (1.0, 0.589256862745098, 0.0130736618971914),
    'black',
    (0.31,0.443,0.745),]

    linetype = ['-.', '-', '--', ':', ':' ,':']
    markertype = ['o', '|', '+', 'x']

    X_max = -1

    for i, data in enumerate(datas):
        X, Y = cdf_transfer(data)
        plt.plot(X,Y, linetype[i%len(linetype)], color=colors[i%len(colors)], label=linelabels[i], linewidth=1.2)#, marker = markertype[i%len(markertype)])
        X_max = max(X_max, max(X))

    plt.ylim(0, 1)
    plt.yticks([0.00, 0.25, 0.50, 0.75, 1.00], fontsize=_fontsize)
    plt.xticks(fontsize=_fontsize)

    #plt.gca().xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

    # plt.grid(linestyle = ':' ,linewidth = 1)

    legend_properties = {'size':_fontsize}

    plt.legend(
        #loc = 'upper left',#'lower right',
        # bbox_to_anchor=(1, 0.75),
        handletextpad=0.4,
        bbox_to_anchor=(0.5, 0.52),
        prop = legend_properties,
        handlelength=1.5,
        frameon = False)

    ax.tick_params(axis="both", direction="in", length = 2, width = 1)

    # Remove frame top and right
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    #plt.tight_layout(pad=0.1, w_pad=0.01, h_pad=0.01)

    #ax.set_xscale('log')
    plt.tight_layout(pad=0.2, w_pad=0.01, h_pad=0.01)

    #plt.xlim(0, 1.21e6)#, 150)
    #plt.xlim(0, 1.0)
    #plt.xlim(0, 2000)
    #plt.show()

    plt.savefig(name)

sumOfSamples = [3984, 9494, 10567, 119775, 30, 139630, 846, 7458, 119235, 2827, 15654, 7764, 69, 14148, 334049, 20900, 17541, 112457, 44601, 56189, 6501, 1223, 112900, 600, 34485, 22314, 129705, 8043, 66634, 5, 162, 28211, 52653, 83819, 9987, 385, 80555, 477, 7006, 10855, 11311, 13686, 87199, 11455, 12777, 1357, 19791, 138493, 3634, 37667, 13822, 1574, 37974, 66294, 329, 5590, 14095, 14495, 64045, 4000, 61153, 11058, 28735, 311562, 7831, 1262, 33254, 45245, 13900, 5714, 29812, 37868, 69, 15118, 1082, 97, 163225, 8698, 61327, 55033, 17444, 678008, 245418, 80, 2113, 2364, 535410, 168260, 27475, 12887, 1870, 7866, 28231, 4651, 162355, 4667, 30228, 2169, 1230, 9044, 488395, 45387, 313394, 18431, 265536, 2418, 96739, 963, 11139, 956, 10463, 3468, 17810, 21779, 1083, 3268, 140525, 22490, 46332, 109924, 7208, 126088, 24129, 20751, 127823, 1597, 17602, 1221, 16221, 16074, 78117, 46854, 69, 1422, 46973, 8272, 42355, 3197, 77, 39499, 12821, 1883, 93385, 942, 2788, 68582, 438828, 53330, 138654, 65650]

plot_cdf([sumOfSamples], [''], "\# of Samples per Client", "CDF", "sizeImg.pdf")
#plot_cdf([divBigger], [''], "Data Divergence across Countries", "CDF", "cDiv.pdf")
