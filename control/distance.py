# path : ((real,real), (real,real) array) -> real
# path is all the points that we want to consider for distance
# Returns the shortest distance from pos to path

import math

def distance(pos, path):
    #find minimum distance to point
    d = distanceToPoint(pos,path[0])
    for point in path[1:] :
        d = min(d,distanceToPoint(pos,point))

    #find minimum distance to line
    for i in range(len(path)-1):
        p1 = path[i]
        p2 = path[i+1]
        d = min(d,shortestDistanceToLine(pos,p1,p2,d))

    return d

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
        return height

    negative_height = (-1*height_vector_x,-1*height_vector_y)
    if(checkOnLine(source,negative_height,p1,p2)):
        return height

    return default_return




