import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pathlib
import random
from copy import deepcopy
import util


def newAnt(pos, dir, hasFood=False, action=None):
    return {
        "pos": pos,
        "dir": dir,
        "str": 0,
        "hasFood": hasFood,
        "alive": True,
        "action": action,
    }


def newPh(pos, val):
    return {"pos": pos, "val": val}


def dir2theta(dir):
    # return np.arctan(dir[1] / dir[0])
    return np.arctan2(dir[1], dir[0])


def theta2dir(theta):
    return np.array([np.cos(theta), np.sin(theta)])


def randTheta(x):
    return random.uniform(-x, x)


# def randDir(x):
#     return theta2dir(random.uniform(-x, x))


class antSys:
    def __init__(self, params):
        self.params = params
        # self.params["dirName"].mkdir(parents=True, exist_ok=True)
        np.random.seed(params["seed"])
        random.seed(params["seed"])

        self.antTS = [[]]  # time series of ants
        self.phTS = [[]]  # time series of pheromone
        self.foodTS = [[]]  # time series of food
        self.saitanTS = []
        self.esaariTS=[]

        self.nestPos = np.array(self.params["nestPos"])
        self.numCollectedFood = 0

        logName = str(pathlib.Path(__file__).parent / "figures/log.txt")
        self.f = open(logName, "w")

    '''
    DISTURBANCE MODEL
    '''
    #def disturbance(self):
    #   if self.params['disturbance'] == "antPosNegative":
    #      grid = 

    '''
    ANT-PHEROMONE MODEL
    '''

    def distributeFood(self):
        for _ in range(self.params["foodNum"]):
            self.foodTS[-1].append(self.newFoodLoc())

    def newFoodLoc(self):
        return np.array([random.uniform(10, 40), random.uniform(10, 40)])

    def run(self):
        self.distributeFood()
        for t in range(self.params["T"]):
            print(f"----- time {t+1} -----", file=self.f)
            self.update()
        self.printAntTS()
        self.f.close()

    def update(self):
        self.deepCopyLast()  # 最新状態をコピーして時系列の最後に配置
        #print(self.saitanTS)
        #print(self.antTS)
        #print('\n')
        self.makerinsetu()
        for ant in self.antTS[-1]:  # 存在する全てのアリに対して
            print(ant, file=self.f)
            ant["action"] = None

            if self.isTootired(ant):  # if too tired
                self.kill(ant)
            # elif self.isCloseToAnotherAnt(ant):  # if too close to another ant
            #     self.avoid(ant)
            elif self.isCloseToWall(ant):
                self.avoidWall(ant)
            elif ant["hasFood"] is True:  # if has food
                self.leavePh(ant, "hasFood")
                if self.isVeryCloseToNest(ant):
                    self.goBackToNest(ant)
                elif self.isCloseToNest(ant):
                    self.goTowardNest(ant)
                else:
                    self.move(ant)
            elif self.isTired(ant):  # if tired
                self.leavePh(ant, "tired")
                if self.isVeryCloseToNest(ant):
                    self.goBackToNest(ant)
                elif self.isCloseToNest(ant):
                    self.goTowardNest(ant)
                else:
                    self.move(ant)
            else:  # mainly if doesn't have food
                if self.isVeryCloseToFood(ant):
                    self.getFood(ant)
                elif self.isCloseToFood(ant):
                    self.goTowardFood(ant)
                else:
                    self.move(ant)

            print(ant, file=self.f)
        
        self.aritrailstock()
        # 生きているアリだけを残す
        self.antTS[-1] = deepcopy(
            [ant for ant in self.antTS[-1] if ant["alive"] is True]
        )

        self.antGeneration()  # ランダムにアリを生成
        self.evaporate()  # フェロモンが揮発

    def deepCopyLast(self):
        for list in [
            self.antTS,
            self.foodTS,
            self.phTS,
        ]:  
            #print(list)
            list.append(deepcopy(list[-1]))

    def isTootired(self, ant):
        return ant["str"] > self.params["isTooTiredThreshold"]

    def kill(self, ant):
        if ant["hasFood"] is True:
            self.foodTS[-1].append(ant["pos"])
        ant["alive"] = False
        ant["action"] = "killed"
        print("ant killed", file=self.f)

    def incrementStrain(self, ant):
        ant["str"] += 1

    def isCloseToRightWall(self, ant):
        return ant['pos'][0] + self.params['velocity'] + 1 > self.params['xlim'][1]

    def isCloseToLeftWall(self, ant):
        return ant['pos'][0] - self.params['velocity'] - 1 < self.params['xlim'][0]

    def isCloseToUpWall(self, ant):
        return ant['pos'][1] + self.params['velocity'] + 1 > self.params['ylim'][1]

    def isCloseToDownWall(self, ant):
        return ant['pos'][1] - self.params['velocity'] - 1 < self.params['ylim'][0]

    def isCloseToWall(self, ant):
        return self.isCloseToDownWall(ant) or self.isCloseToUpWall(ant) or self.isCloseToLeftWall(ant) or self.isCloseToRightWall(ant)

    def avoidWall(self, ant):
        nextPos = deepcopy(ant['pos'])
        if self.isCloseToRightWall(ant):
            nextPos[0] = self.params['xlim'][1] - self.params['velocity'] - 1
        if self.isCloseToLeftWall(ant):
            nextPos[0] = self.params['xlim'][0] + self.params['velocity'] + 1
        if self.isCloseToDownWall(ant):
            nextPos[1] = self.params['ylim'][0] + self.params['velocity'] + 1
        if self.isCloseToUpWall(ant):
            nextPos[1] = self.params['ylim'][1] - self.params['velocity'] - 1
        ant['dir'] = util.unit_vector(nextPos-ant['pos'])
        ant['pos'] = nextPos

    def leavePh(self, ant, type):
        if random.uniform(0, 1) < self.params[type + "PheromoneProb"]:
            self.phTS[-1].append(
                newPh(pos=ant["pos"],
                      val=self.params[type + "PheromoneAmount"])
            )

    def isVeryCloseToNest(self, ant):
        return np.linalg.norm(ant["pos"] - self.nestPos) < self.params["velocity"]

    def isCloseToNest(self, ant):
        return np.linalg.norm(ant["pos"] - self.nestPos) < self.params["pheromone_R"]

    def goBackToNest(self, ant):
        # self.leavePh(ant, "closeToNest") # goBackToNestでは分泌しない
        ant["alive"] = False
        ant["action"] = "cameBackToNest"
        if ant["hasFood"] is True:
            self.numCollectedFood += 1
            print("food carried in", file=self.f)

    def goTowardNest(self, ant):
        dir = util.unit_vector(self.params["nestPos"] - ant["pos"])
        nextDir = theta2dir(
            dir2theta(ant["dir"] + dir)
            + randTheta(self.params["goTowardNestRandomTheta"])
        )
        nextDir = util.unit_vector(nextDir)
        ant["pos"] += self.params["velocity"] * nextDir
        ant["dir"] = nextDir
        ant["action"] = "goingTowardNest"
        self.leavePh(ant, "closeToNest")  # goTowardNestでは移動後に分泌

    def move(self, ant):
        if self.anyPhIsInSight(ant):
            self.followPh(ant)
        else:
            self.searchAtRandom(ant)

    def anyPhIsInSight(self, ant):
        for ph in self.phTS[-1]:
            if self.thePhIsInSight(ant, ph):
                return True
        return False

    def thePhIsInSight(self, ant, ph):
        relPos = ph["pos"] - ant["pos"]
        return (
            0 < np.linalg.norm(relPos) < self.params["pheromone_R"]
            and util.angle_between(ant["dir"], relPos) < self.params["sightAngle"]
        )

    def followPh(self, ant):
        self.leavePh(ant, "followPheromone")  # followPhでは移動前に分泌
        phDir = np.zeros(2)
        for ph in self.phTS[-1]:
            if self.thePhIsInSight(ant, ph):
                relPos = ph["pos"] - ant["pos"]
                phDir += util.unit_vector(relPos)
        print("phDir", file=self.f)
        print(phDir, file=self.f)
        nextDir = theta2dir(
            dir2theta(util.unit_vector(phDir))
            + randTheta(
                self.params["followPhRandomTheta"]
            )  # followPhでは（今の計算式）＋(-15, 15)
        )
        print("nextDir", file=self.f)
        print(nextDir, file=self.f)
        ant["pos"] += self.params["velocity"] * nextDir
        ant["dir"] = nextDir
        ant["action"] = "followingPheromone"
        self.incrementStrain(ant)

    def searchAtRandom(self, ant):
        theta = randTheta(self.params["randomRotation"])
        nextDir = theta2dir(theta + dir2theta(ant["dir"]))
        ant["pos"] += self.params["velocity"] * nextDir
        ant["dir"] = nextDir
        ant["action"] = "searchingAtRandom"
        self.incrementStrain(ant)
        self.leavePh(ant, "searchAtRandom")  # searchAtRandomでは移動後に分泌
        # 餌を持っていない場合のsearchAtRandomでは移動後にさらに20％の確率で10の量の”探索中”のフェロモンを分泌
        if ant["hasFood"] is False:
            self.leavePh(ant, "searching")

    def isTired(self, ant):
        return ant["str"] > self.params["isTiredThreshold"]

    def isCloseToFood(self, ant):
        if len(self.foodTS[-1]) == 0:
            return False
        else:
            return np.any(self.relDistToFood(ant) < self.params["pheromone_R"])

    def isVeryCloseToFood(self, ant):
        if len(self.foodTS[-1]) == 0:
            return False
        else:
            return np.any(self.relDistToFood(ant) < self.params["velocity"])

    def relDistToFood(self, ant):
        relPos = np.array(self.foodTS[-1]) - ant["pos"]
        return np.linalg.norm(relPos, axis=1)

    def getFood(self, ant):
        print("self.foodTS[-1][self.closestFoodIdx(ant)]", file=self.f)
        print(self.foodTS[-1][self.closestFoodIdx(ant)], file=self.f)
        # self.leavePh(ant, "findFood") # getFoodでは分泌しない
        del self.foodTS[-1][self.closestFoodIdx(ant)]
        ant["hasFood"] = True
        print("food picked", file=self.f)
        ant["dir"] = -ant["dir"]
        ant["action"] = "gotFood"
        self.incrementStrain(ant)

    def goTowardFood(self, ant):
        relPos = self.foodTS[-1][self.closestFoodIdx(ant)] - ant["pos"]
        nextDir = util.unit_vector(ant["dir"] + util.unit_vector(relPos))
        ant["pos"] += self.params["velocity"] * nextDir
        ant["dir"] = nextDir
        ant["action"] = "goingTowardFood"
        self.incrementStrain(ant)
        self.leavePh(ant, "findFood")  # goTowardFoodでは移動後に分泌

    def closestFoodIdx(self, ant):
        return np.argmin(self.relDistToFood(ant))

    def antGeneration(self):
        if (
            random.uniform(0, 1) < self.params["antGenerationProb"]
            and len(self.antTS[-1]) < self.params["maxAntNum"]
        ):
            print("ant generated", file=self.f)
            theta = randTheta(np.pi)
            self.antTS[-1].append(
                newAnt(pos=self.nestPos, dir=theta2dir(
                    theta), action="generated")
            )

    def evaporate(self):
        if len(self.phTS) % self.params["evaporationPeriod"] == 0:
            for ph in self.phTS[-1]:
                ph["val"] -= self.params["pheromoneEvaporation"]
            self.phTS[-1] = [
                ph
                for ph in self.phTS[-1]
                if ph["val"] >= self.params["pheromoneRemoveThreshold"]
            ]

    def printAntTS(self):
        print("ANT TIME SERIES", file=self.f)
        for t in range(self.params["T"] + 1):
            print(f"----- time {t} -----", file=self.f)
            for ant in self.antTS[t]:
                print(ant["pos"], file=self.f)
    def makerinsetu(self):
        mylist=[[0,0]]
        dir=0
        esatika=0
        dirbuf=[]
        kari=0
        for ph in self.phTS[-1]:
            mylist.append([ph["pos"][0],ph["pos"][1]])
            if (ph["pos"][0]>0 and ph["pos"][1]>0) and (ph["pos"][0]**2+ph["pos"][1]**2)>dir:
                dir=ph["pos"][0]**2+ph["pos"][1]**2
                esatika=kari+1
            kari += 1

        rinsetu = [[0 for i in range(len(mylist))] for j in range(len(mylist))]

        for i in range(len(mylist)):
            for j in range(len(mylist)):
                if (np.sqrt((mylist[i][0] - mylist[j][0])**2 + (mylist[i][1] - mylist[j][1])**2)) < self.params["pheromone_R"]:
                    rinsetu[i][j] = np.sqrt((mylist[i][0] - mylist[j][0])**2 + (mylist[i][1] - mylist[j][1])**2)
        arr_1d = np.array(rinsetu)
        G = nx.from_numpy_matrix(arr_1d)
        #nx.draw(G, with_labels=True)
        #plt.show()
        k=[np.array([0,0])]
        if nx.has_path(G, source=0, target=esatika) :
            saikei=nx.shortest_path(G,source=0,target=esatika)
            nya=0
            for i in range(len(saikei)):
                k.append(np.array([mylist[saikei[i]][0],mylist[saikei[i]][1]]))
        self.saitanTS.append(k)
        #print(self.saitanTS)

    def aritrailstock(self):
        p=self.antTS
        antlist=[]
        ssk=0
        k=[np.array([0,0])]
        for i in range(len(self.antTS[-1])):
            antlist.append(self.antTS[-1][i])
            if(self.antTS[-1][i]["action"]== "gotFood"):
                esaa=self.antTS[-1][i]["str"]
                #print(esaa)
                #print(len(self.antTS)-1)
                for j in range(0, len(self.antTS)-1)[::-1]:
                    #print(j)
                    for mn in self.antTS[j]:
                        #print(mn)
                        if(mn["str"]==esaa-1):
                            k.append(np.array([mn["pos"][0],mn["pos"][1]]))
                            break
                    esaa-=1
                    if(esaa==0):
                        break
                #print(k)
                ssk+=1
                break
        if(ssk==0 and len(self.esaariTS)>0):
            k=deepcopy(self.esaariTS[-1])
        self.esaariTS.append(k)


