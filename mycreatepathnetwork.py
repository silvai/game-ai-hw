'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

from core import *
import numpy as np

# Creates a path node network that connects the midpoints of each nav mesh together
def myCreatePathNetwork(world, agent=None):
    nodes = []
    edges = []
    polys = []

    ### YOUR CODE GOES BELOW HERE ###
    lines = []
    points = world.getPoints()
    obstacles = world.getObstacles()

    ######## Get the poly lines #########

    for point1 in points:
        for point2 in points:
            for point3 in points:
                if point1 != point2 and point2 != point3 and point1 != point3:
                    if (point1, point2, point3) not in lines and (point1, point3, point2) not in lines \
                            and (point2, point1, point3) not in lines and (point2, point3, point1) not in lines \
                            and (point3, point2, point1) not in lines and (point3, point1, point2) not in lines:
                        if not obstructed(point1, point2, world) and not obstructed(point2, point3, world) and not obstructed(point1, point3, world):
                            lines.append((point1, point2, point3))

    triangles = []
    for l in lines:
        if l not in triangles:
            triangles.append(l)

    #
    # ######## Use triangles to form polygons ########
    #
    for t in range(0, len(triangles) - 1, 2):
        if triangles[t] != triangles[t+1]:
            if polygonsAdjacent(triangles[t], triangles[t+1]):
                merged = combinePolys(triangles[t], triangles[t+1])
                if isConvex(merged) and merged not in polys:
                    polys.append(merged)

    for p in polys:
        if obstructedByPolys(p, world):
            p[0] = (0, 0)
            p[1] = (0, 0)
            p[2] = (0, 0)
            p[3] = (0, 0)

    print polys


    #
    # for l in range(len(polys)):
    #     for i in range(3):
    #         if obstructed(polys[l][i], polys[l][i], world):
    #             polys[l][i] = (0, 0)
    #     x = polys[l][0]
    #     y = polys[l][1]
    #     z = polys[l][2] #not really a z coord, just the next vertex of the polygon
    #     a = polys[l][3]
    #     if obstructed(x, y, world):
    #         print "obstruction"
    #         polys[l] = ((0, 0), (0, 0), (0, 0))
    #     if obstructed(x, z, world):
    #         polys[l] = ((0, 0), (0, 0), (0, 0))
    #     if obstructed(x, a, world):
    #         polys[l] = ((0, 0), (0, 0), (0, 0))
    #     if obstructed(z, y, world):
    #         polys[l] = ((0, 0), (0, 0), (0, 0))
    #     if obstructed(z, a, world):
    #         polys[l] = ((0, 0), (0, 0), (0, 0))
    # # # ######## Create edges using polygon midpoints ########
    #
    # midpoints = []
    # for t in range(0, len(polys) - 1, 2):
    #     if polys[t] != polys[t+1]:
    #         commonEdge = polygonsAdjacent(polys[t], polys[t+1])
    #         if commonEdge:
    #             for e in commonEdge:
    #                 for e2 in commonEdge:
    #                     if e != e2:
    #                         midpoint = getMidpoint(e, e2)
    #                         if midpoint not in midpoints:
    #                             midpoints.append(midpoint)

    #
    # for m in range(0, len(midpoints) - 1, 2):
    #     if not obstructed(midpoints[m], midpoints[m+1], world):
    #         edges.append((midpoints[m], midpoints[m+1]))

    # ####### Make sure that the edges are agent radius away from each obstacle ########
    # #
    # for mp in midpoints:
    #     for mp2 in midpoints:
    #         for obstacle in obstacles:
    #             for oPoint in obstacle.getPoints():
    #                 if minimumDistance((mp, mp2), oPoint) > agent.getMaxRadius():
    #                     if not obstructed(mp, mp2, world):
    #                         edges.append((mp, mp2))

    # myBuildPathNetwork(nodes, world, agent)

    ### YOUR CODE GOES ABOVE HERE ###
    return nodes, edges, polys



def obstructed(p1, p2, world):
    obstacles = world.getObstacles()
    if rayTraceWorldNoEndPoints(p1, p2, world.getLines()):
        return True
    for obstacle in obstacles:
        if pointInsidePolygonPoints(p1, obstacle.getPoints()) and pointInsidePolygonPoints(p2, obstacle.getPoints()):
            return True
        if pointInsidePolygonLines(p1, obstacle.getLines()) and pointInsidePolygonLines(p2, obstacle.getLines()):
            return True
        if pointInsidePolygonPoints(getMidpoint(p1, p2), obstacle.getPoints()):
            return True

    return False

def obstructedByPolys(polys, world):
    obstacles = world.getObstacles()

    for obstacle in obstacles:
        # check combined poly's avg vertices / midvertices
        points1 = obstacle.getPoints()
        avgX = 0
        avgY = 0
        for p in points1:
            avgX += (p[0])
            avgY += (p[1])
        avgX /= (len(points1))
        avgY /= (len(points1))

        if pointInsidePolygonPoints((avgX, avgY), polys):
            return True

def combinePolys(poly1, poly2):

    points1 = []
    for p in poly1:
        #for p in line:
            points1.append(p)
    for p in poly2:
        #for p in line:
            if p not in points1:
                points1.append(p)
    points1.sort()

    # Find average of vertices to choose starting point
    avgX = 0
    avgY = 0
    for p in points1:
        avgX += (p[0])
        avgY += (p[1])
    avgX /= (len(points1))
    avgY /= (len(points1))
    avgVertex = (avgX, avgY)

    # then compute the angle of each vertex to the center point
    angles = []
    dict = {}
    for p in points1:
        angle = math.atan2(avgY - p[1], avgX - p[0])
        angles.append(angle)
        # set dict keys
        dict[angle] = (p[0], p[1])
    angles.sort()
    points = []
    for t in angles:
        points.append(dict[t])

    return points


# def angle_between(p1, p2):
#     return np.arccos(np.clip(np.dot(p1, p2), -1.0, 1.0))


def getMidpoint(p1, p2):
    # p1 = line[0]
    # p2 = line[1]
    x = ((p1[0] + p2[0]) / 2)
    y = ((p1[1] + p2[1]) / 2)
    return (x, y)


# Copy Pasta from Homework 2
def myBuildPathNetwork(pathnodes, world, agent=None):
    lines = []
    agentSize = agent.getMaxRadius()
    obstacles = world.getPoints()
    for n in range(0, len(pathnodes) - 1):
        for i in range(n + 1, len(pathnodes)):
            node = pathnodes[n]
            nextNode = pathnodes[i]
            lines.append((node, nextNode))
    for n in range(0, len(lines)):
        rayTraceTup = rayTraceWorld(lines[n][0], lines[n][1], world.getLinesWithoutBorders())
        if rayTraceTup:
            lines[n] = ((0, 0), (0, 0))
        for o in obstacles:
            if minimumDistance(lines[n], o) < agentSize / 2:
                lines[n] = ((0, 0), (0, 0))
    return lines
