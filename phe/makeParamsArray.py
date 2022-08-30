import copy
import json
import numpy as np
from pathlib import Path
import util.misc
import itertools
import shutil
import os


def makeParamsArray(jsonfile, DEMO):
    gifPeriod = 10

    if DEMO is True:
        rootDataDir = r"C:/Dropbox/Download"
    else:
        rootDataDir = r"C:/GDrive/2021-10-18_SS"

    dataDir = Path(rootDataDir).resolve() / \
        "data" / util.misc.timestr()
    dataDir.mkdir(exist_ok=True, parents=True)

    # os.makedirs(os.path.dirname(dataDir), exist_ok=True)
    shutil.copyfile(jsonfile, dataDir/jsonfile.name)

    with jsonfile.open(encoding="utf-8") as f:
        parameters = json.load(f)
    globals().update(parameters)

    paramsSeedArray = [{
        'N1': N,
        'N2': N,
        'tau': tau,
        'grav': grav,
        'dim': dim,
        'T': T,
        'vmax': vmax,
        'seed': 1,
        'R': R,
        'paramxx': {'R': R, 'Watt': Wattxx, 'Wrep': Wrep, 'Wali': Walixx},
        'paramxy': {'R': R, 'Watt': 0, 'Wrep': Wrep, 'Wali': 0},
        'paramyx': {'R': R, 'Watt': 0, 'Wrep': Wrep, 'Wali': 0},
        'dirName': dataDir /
        f"N{N}_T{T}_R{R}_Wrep{Wrep:.5g}_Wattxx{Wattxx:.5g}_Walixx{Walixx:.5g}_vmax{vmax:.5g}_grav{grav:.5g}",
        'gifPeriod': gifPeriod
    }
        for vmax in vmaxArray
        for Wattxx in WattxxArray
        for grav in gravArray
        for Wrep in WrepArray
        for Walixx in WalixxArray
        for N in NArray
        for R in RArray]

    paramsArray = []
    for paramsSeed in paramsSeedArray:
        WattyyArray = paramsSeed['paramxx']['Watt'] * \
            np.logspace(WattyyRange[0], WattyyRange[1], WattyyDiv)
        WaliyyArray = paramsSeed['paramxx']['Wali'] * \
            np.logspace(WaliyyRange[0], WaliyyRange[1], WaliyyDiv)
        for (Wattyy, Waliyy) in itertools.product(WattyyArray, WaliyyArray):
            paramsArray.append(copy.deepcopy(paramsSeed))
            paramyy = {
                'R': paramsSeed['paramxx']['R'],
                'Watt': Wattyy,
                'Wrep': paramsSeed['paramxx']['Wrep'],
                'Wali': Waliyy
            }
            diffparams = {
                'paramyy': paramyy,
                'fname': f"Wattyy{Wattyy:.3g}Waliyy{Waliyy:.3g}"
            }
            paramsArray[-1].update(diffparams)
    return paramsArray
