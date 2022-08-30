import subprocess
import matplotlib.pyplot as plt
import matplotlib.patches as patches

MARKERSIZE = 1
FIGSIZE = (8, 6)
DPI = 150


def snapshot(AS, t, ax=None, open=True, save=False, new=True):
    if ax is None:
        fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
        ax = fig.add_subplot(1, 1, 1)
    if new:
        ax.lines = []
        ax.patches = []
    food_snapshot(AS, t, ax)
    ph_snapshot(AS, t, ax)
    ant_snapshot(AS, t, ax)
    saitan_snapshot(AS, t, ax)
    nest(AS, ax)
    wall(AS, ax)
    pngName = f"figures/{t}.png"
    if save:
        plt.savefig(pngName)
        if open:
            subprocess.Popen(["start", pngName], shell=True)


def snapshot2(AS, t):
    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["ytick.direction"] = "in"

    # fig.add_subplot(1, 1, 1)

    plt.plot(AS.params["nestPos"][0], AS.params["nestPos"][0], "kx")

    xy = (AS.params["xlim"][0], AS.params["ylim"][0])
    width = AS.params["xlim"][1] - AS.params["xlim"][0]
    height = AS.params["ylim"][1] - AS.params["ylim"][0]
    patches.Rectangle(xy=xy, width=width, height=height, ec="#000000", fill=False)
    # plt.add_patch(r)

    x = [ant["pos"][0] for ant in AS.antTS[t]]
    y = [ant["pos"][1] for ant in AS.antTS[t]]
    plt.plot(x, y, "ko", markersize=MARKERSIZE)

    x = [ph["pos"][0] for ph in AS.phTS[t]]
    y = [ph["pos"][1] for ph in AS.phTS[t]]
    plt.plot(x, y, "bo", markersize=MARKERSIZE)

    x = [food[0] for food in AS.foodTS[t]]
    y = [food[1] for food in AS.foodTS[t]]
    plt.plot(x, y, "yo", markersize=MARKERSIZE)

    x = [saitan[0] for saitan in AS.saitanTS[t]]
    y = [saitan[1] for saitan in AS.saitanTS[t]]
    plt.plot(x, y, "so", markersize=MARKERSIZE)
    # return im


def openfile(fname, flag=False):
    if flag:
        subprocess.Popen(["start", fname], shell=True)


def nest(AS, ax):
    ax.plot(AS.params["nestPos"][0], AS.params["nestPos"][0], "kx")


def wall(AS, ax):
    xy = (AS.params["xlim"][0], AS.params["ylim"][0])
    width = AS.params["xlim"][1] - AS.params["xlim"][0]
    height = AS.params["ylim"][1] - AS.params["ylim"][0]
    r = patches.Rectangle(xy=xy, width=width, height=height, ec="#000000", fill=False)
    ax.add_patch(r)


def ant_snapshot(AS, t, ax):
    x = [ant["pos"][0] for ant in AS.antTS[t]]
    y = [ant["pos"][1] for ant in AS.antTS[t]]
    ax.plot(x, y, "ko", markersize=MARKERSIZE)


def ph_snapshot(AS, t, ax):
    x = [ph["pos"][0] for ph in AS.phTS[t]]
    y = [ph["pos"][1] for ph in AS.phTS[t]]
    ax.plot(x, y, "bo", markersize=MARKERSIZE)


def food_snapshot(AS, t, ax):
    x = [food[0] for food in AS.foodTS[t]]
    y = [food[1] for food in AS.foodTS[t]]
    ax.plot(x, y, "yo", markersize=MARKERSIZE)

def saitan_snapshot(AS, t, ax):
    x = [saitan[0] for saitan in AS.saitanTS[t]]
    y = [saitan[1] for saitan in AS.saitanTS[t]]
    ax.plot(x, y, "so", markersize=MARKERSIZE)
