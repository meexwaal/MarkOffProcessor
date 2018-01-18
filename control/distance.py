# path : ((real,real), (real,real) array, (real,real)) -> real
# path is all the points that we want to consider for distance
# Returns the shortest distance from pos to path

import math

def distance(pos, path, rotation):
    #find minimum distance to point
    d = distanceToPoint(pos,path[0])
    shortest_point_index = 0;
    distance_vector = resultantVector(pos,path[0])
    for i in range(1,len(path)):
        dist_test = distanceToPoint(pos,path[i])
        if dist_test < d:
            d = dist_test
            distance_vector = resultantVector(pos,path[i])
            shortest_point_index = i;

    shortest_distance_to_point = d;

    #find minimum distance to line
    for i in range(len(path)-1):
        p1 = path[i]
        p2 = path[i+1]
        dist_test = shortestDistanceToLine(pos,p1,p2,distance_vector)
        dist_test_magnitude = distanceToPoint((0,0),dist_test)
        if dist_test_magnitude < d:
            distance_vector = dist_test
            d = dist_test_magnitude

    if cross_product_positive(distance_vector,rotation):
        return d , shortest_distance_to_point , shortest_point_index
    else: return -1*d , shortest_distance_to_point , shortest_point_index

def negative_vector(v):
    return (-1*v[0],-1*v[1])

def cross_product_positive(v1,v2):
    #expects 2D vectors
    return v1[0]*v2[1] - v1[1]*v2[0] > 0

def resultantVector(p1,p2):
    return (p2[0] - p1[0], p2[1] - p1[1])

def distanceToPoint(source,target):
    #calculates distance between location and target
    return math.sqrt((source[0]-target[0])**2 + (source[1]-target[1])**2)

def checkOnLine(source,vector,line_p1, line_p2):
    x1,x2 = line_p1[0],line_p2[0]
    y1,y2 = line_p1[1],line_p2[1]

    check_x = source[0]+vector[0]
    check_y = source[1]+vector[1]

    return (min(x1,x2) <= check_x <= max(x1,x2) and 
            min(y1,y2) <= check_y <= max(y1,y2))

def shortestDistanceToLine(source,p1,p2,default_return):
    #default return because there is no return value if shortest distance isn't on line seg
    #source is robot position
    #p1 and p2 points on the line
    x0,y0 = source[0],source[1]
    x1,x2 = p1[0],p2[0]
    y1,y2 = p1[1],p2[1]

    #find base, height, and area of triangle
    area = abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1) / 2
    base = distanceToPoint(p1,p2)
    height =  2*area / base 

    #divide by base to normalize
    base_vector_x = (x2-x1) / base
    base_vector_y = (y2-y1) / base

    #perpendicular to base vector
    height_vector_x = -1*base_vector_y * height
    height_vector_y = base_vector_x * height
    height_vector = (height_vector_x,height_vector_y)

    #try both height_vector directions from source and see if they are on the line
    if(checkOnLine(source,height_vector,p1,p2)): 
        return height_vector

    negative_height = negative_vector(height_vector)
    if(checkOnLine(source,negative_height,p1,p2)):
        return negative_height

    return default_return




