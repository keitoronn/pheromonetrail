import model
import video
import numpy as np

params = {
    "seed": 1,
    "nestPos": [0.0, 0.0],
    "foodNum": 50,
    "T": 300,
    "pheromoneEvaporation": 1.0,
    "pheromoneRemoveThreshold": 1.0,
    "antGenerationProb": 0.2,
    "maxAntNum": 100,
    "isTiredThreshold": 200.0,
    "isTooTiredThreshold": 300.0,
    "pheromone_R": 8.0,
    # pheromone 認知に使用 KKE websiteによると60が妥当か．180だとアリが餌をとりにいかない
    "sightAngle": np.pi / 180 * 60,
    "velocity": 1.0,
    "searchAtRandomPheromoneProb": 0.5,
    "searchAtRandomPheromoneAmount": 10.0,
    "followPheromonePheromoneProb": 0.2,
    "followPheromonePheromoneAmount": 10.0,
    "hasFoodPheromoneProb": 0.2,
    "hasFoodPheromoneAmount": 15.0,
    "tiredPheromoneProb": 0.2,
    "tiredPheromoneAmount": 10.0,
    "findFoodPheromoneProb": 0.2,
    "findFoodPheromoneAmount": 10.0,
    "closeToNestPheromoneProb": 0.5,
    "closeToNestPheromoneAmount": 10.0,
    "evaporationPeriod": 4,
    "randomRotation": np.pi / 180 * 30,
    "searchingPheromoneProb": 0.2,  # 餌を持っていない場合のsearchAtRandomでは移動後にさらに20％の確率で
    "searchingPheromoneAmount": 10.0,  # 10の量の”探索中”のフェロモンを分泌
    # goTowardNestでは（今の計算式）＋(-10, 10)
    "goTowardNestRandomTheta": np.pi / 180 * 10,
    "followPhRandomTheta": np.pi / 180 * 15,  # followPhでは（今の計算式）＋(-15, 15)
    "xlim": (-50, 50),
    'ylim': (-50, 50),
    'disturbance': 'antPosNegative'
}

# def funcCompareTime(params, open=False):
#     myModel = model.SS(params)
#     with util.misc.timer():
#         myModel.run()
#     myModel = model.SS(params)
#     with util.misc.timer():
#         myModel.run_numba()


# def func(params, open=False):
#     start = time.perf_counter()
#     myModel = model.SS(params)
#     myModel.run_numba_components()
#     picture.plot_swarm_trajectories(myModel, open=open)
#     video.swarm(myModel, open=open)
#     del myModel
#     print('Elapsed:', time.perf_counter() - start)


def main():
    myModel = model.antSys(params)
    myModel.run()
    print(myModel.numCollectedFood)
    video.main_animation(myModel)


if __name__ == "__main__":
    main()
