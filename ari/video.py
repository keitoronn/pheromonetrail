import matplotlib.pyplot as plt
from celluloid import Camera
import picture
import subprocess
import pathlib
import matplotlib.animation as animation

# import matplotlib.pyplot as plt
import matplotlib.patches as patches
import copy

MARKERSIZE = 1
FIGSIZE = (8, 6)
DPI = 150


def main_celluloid(AS, open=False):
    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["ytick.direction"] = "in"

    fig = plt.figure(figsize=(3, 3), dpi=300)
    camera = Camera(fig)

    for t in range(0, AS.params["T"]):
        ax = fig.add_subplot(1, 1, 1)
        picture.snapshot(AS, t, ax, open=False, save=False, new=False)
        camera.snap()

    # fig.suptitle(
    #     f"Wattyy={AS.params['paramyy']['Watt']:.2g}, Waliyy={AS.params['paramyy']['Wali']:.2g}"
    # )
    gifName = str(pathlib.Path(__file__).parent / "figures/video.gif")
    print(gifName)
    camera.animate().save(gifName)
    if open:
        subprocess.Popen(["start", gifName], shell=True)


def main_animation(AS):
    fig = plt.figure(figsize=(3, 3), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    picture.wall(AS, ax)
    artists = []
    for t in range(0, AS.params["T"]):
        (nest,) = ax.plot(AS.params["nestPos"][0], AS.params["nestPos"][0], "kx")

        x = [ph["pos"][0] for ph in AS.phTS[t]]
        y = [ph["pos"][1] for ph in AS.phTS[t]]
        (ph,) = ax.plot(x, y, "bo", markersize=MARKERSIZE)

        x = [food[0] for food in AS.foodTS[t]]
        y = [food[1] for food in AS.foodTS[t]]
        (food,) = ax.plot(x, y, "yo", markersize=MARKERSIZE)

        x = [ant["pos"][0] for ant in AS.antTS[t]]
        y = [ant["pos"][1] for ant in AS.antTS[t]]
        (ants,) = ax.plot(x, y, "ko", markersize=MARKERSIZE)

        x = [esaari[0] for esaari in AS.esaariTS[t]]
        y = [esaari[1] for esaari in AS.esaariTS[t]]
        #print(x)
        #print(y)
        (esaari,) = ax.plot(x, y, "ro", markersize=MARKERSIZE*2)

        artists.append([nest, ants, ph, food,esaari])

    ani = animation.ArtistAnimation(fig, artists, interval=100)
    gifName = str(pathlib.Path(__file__).parent / "figures/video.gif")
    mp4Name = str(pathlib.Path(__file__).parent / "figures/video.mp4")
    ani.save(gifName)
    ani.save(mp4Name)

