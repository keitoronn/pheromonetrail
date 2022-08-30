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

        x = [saitan[0] for saitan in AS.saitanTS[t]]
        y = [saitan[1] for saitan in AS.saitanTS[t]]
        #print(x)
        #print(y)
        (saitan,) = ax.plot(x, y, "ro", markersize=MARKERSIZE*2)
        k=[]
        l=[]
        if(len(AS.saitanTS[t])>0):
            p=[]
            q=[]
            for i in range(len(AS.saitanTS[t])-1):
                p.append(AS.saitanTS[t][i])
            for i in range(len(AS.saitanTS[t])-1):
                q.append(AS.saitanTS[t][i+1])

            for i in range(len(AS.saitanTS[t])-1):
                #print(p[i])
                #print(q[i])
                m=[p[i][0],q[i][0]]
                n=[p[i][1],q[i][1]]
                h=ax.plot(m,n,"-or", markersize=0, linewidth=1)
                k.extend(h)
        if(len(AS.saitanTS[t])==2):
            artists.append([nest, ants, ph, food,saitan,k[0]])
        elif(len(AS.saitanTS[t])==3):
            artists.append([nest, ants, ph, food,saitan,k[0],k[1]])
        elif(len(AS.saitanTS[t])==4):
            artists.append([nest, ants, ph, food,saitan,k[0],k[1],k[2]])
        elif(len(AS.saitanTS[t])==5):
            artists.append([nest, ants, ph, food,saitan,k[0],k[1],k[2],k[3]])
        elif(len(AS.saitanTS[t])==6):
            artists.append([nest, ants, ph, food,saitan,k[0],k[1],k[2],k[3],k[4]])
        elif(len(AS.saitanTS[t])==7):
            artists.append([nest, ants, ph, food,saitan,k[0],k[1],k[2],k[3],k[4],k[5]])
        elif(len(AS.saitanTS[t])==8):
            artists.append([nest, ants, ph, food,saitan,k[0],k[1],k[2],k[3],k[4],k[5],k[6]])
        elif(len(AS.saitanTS[t])==9):
            artists.append([nest, ants, ph, food,saitan,k[0],k[1],k[2],k[3],k[4],k[5],k[6],k[7]])
        elif(len(AS.saitanTS[t])==10):
            artists.append([nest, ants, ph, food,saitan,k[0],k[1],k[2],k[3],k[4],k[5],k[6],k[7],k[8]])
        elif(len(AS.saitanTS[t])==11):
            artists.append([nest, ants, ph, food,saitan,k[0],k[1],k[2],k[3],k[4],k[5],k[6],k[7],k[8],k[9]])
        else:
            artists.append([nest, ants, ph, food,saitan])
        #artists.append(k)


    ani = animation.ArtistAnimation(fig, artists, interval=100)
    gifName = str(pathlib.Path(__file__).parent / "figures/video.gif")
    mp4Name = str(pathlib.Path(__file__).parent / "figures/video.mp4")
    ani.save(gifName)
    ani.save(mp4Name)

