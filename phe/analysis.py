import numpy as np

def xyrange(AS):
    x = [ant['pos'][0] for antList in AS.antTS for ant in antList] + [food[0] for foodList in AS.foodTS for food in foodList]
    y = [ant['pos'][1] for antList in AS.antTS for ant in antList] + [food[1] for foodList in AS.foodTS for food in foodList]
    
    AS.xrange = (np.minimum(x), np.maximum(x))
    AS.yrange = (np.minimum(y), np.maximum(y))