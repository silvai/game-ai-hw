# '''
#  * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
#  * Originally developed by Mark Riedl.
#  * Last edited by Mark Riedl 05/2015
#  *
#  * Licensed under the Apache License, Version 2.0 (the "License");
#  * you may not use this file except in compliance with the License.
#  * You may obtain a copy of the License at
#  *
#  *     http://www.apache.org/licenses/LICENSE-2.0
#  *
#  * Unless required by applicable law or agreed to in writing, software
#  * distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.
# '''
#
# import sys, pygame, math, numpy, random, time, copy, operator
# from pygame.locals import *
#
# from constants import *
# from utils import *
# from core import *
#
# # Creates a pathnode network that connects the midpoints of each navmesh together
# def myCreatePathNetwork(world, agent = None):
#     nodes = []
#     edges = []
#     polys = []
#     ### YOUR CODE GOES BELOW HERE ###
#     points = world.getPoints()
#     obstacles = world.getObstacles()
#     temp = []
#     for p1 in points:
#         for p2 in points:
#             for p3 in points:
#                 if p1 == p2 or p1 == p3 or p2 == p3:
#                     continue
#                 if not checkCollision1(world, temp, p1, p2, p3):
#                     temp.append(list((p1, p2, p3)))
#
#     # Get rid of duplicates
#     for t in temp:
#         t.sort()
#         if t not in polys:
#             polys.append(t)
#
#     for n in range(len(polys)):
#         for p1 in polys:
#             for p2 in polys:
#                 if p1 == p2:
#                     continue
#                 if polygonsAdjacent(p1, p2):
#                     # print p1, p2
#                     merged = merge(p1, p2)
#                     # print 'merged: ', merged
#                     if isConvex(merged):
#                         # drawPolygon(merged, world.debug, (0,0,0), 10, False)
#                         polys.remove(p1)
#                         polys.remove(p2)
#                         polys.append(merged)
#                         break
#
#     for p1 in polys:
#         temp = []
#         for p2 in polys:
#             if p1 == p2:
#                 continue
#             common = polygonsAdjacent(p1, p2)
#             if common:
#                 # common = commonPoints(p1, p2)
#                 # print 'common points: ', commonPoints(p1, p2)
#                 mid = midpt(common[0], common[1])
#                 temp.append(mid)
#                 if mid not in nodes:
#                     nodes.append(mid)
#                 # drawCross(world.debug, mid)
#         for i in range(len(temp)):
#             if i == len(temp) - 1:
#                 if checkCollision3(obstacles, temp[i], temp[0], agent):
#                     edges.append((temp[i], temp[0]))
#             else:
#                 if checkCollision3(obstacles, temp[i], temp[i + 1], agent):
#                     edges.append((temp[i], temp[i + 1]))
#
#
#     return nodes, edges, polys
#
#
# def checkCollision1(world, polys, p1, p2, p3):
#     lines = world.getLines()
#     obstacles = world.getObstacles()
#     for p in polys:
#     #     lines.append((p[0], p[1]))
#     #     lines.append((p[0], p[2]))
#     #     lines.append((p[1], p[2]))
#         lines.append(p)
#
#     if (rayTraceWorldNoEndPoints(p2, p3, lines) is not None and (p2, p3) not in lines and (p3, p2) not in lines) or \
#     (rayTraceWorldNoEndPoints(p1, p2, lines) is not None and (p1, p2) not in lines and (p2, p1) not in lines) or \
#     (rayTraceWorldNoEndPoints(p1, p3, lines) is not None and (p1, p3) not in lines and (p3, p1) not in lines):
#         return True
#
#
#     for obstacle in obstacles:
#         mid1 = midpt(p2, p3)
#         mid2 = midpt(p1, p2)
#         mid3 = midpt(p1, p3)
#
#         # Check our triangle inside any of the pre-made obstacles
#         if (pointInsidePolygonLines(mid1, obstacle.getLines()) and (p2, p3) not in lines and (p3, p2) not in lines) or \
#         (pointInsidePolygonLines(mid2, obstacle.getLines()) and (p1, p2) not in lines and (p2, p1) not in lines) or \
#         (pointInsidePolygonLines(mid3, obstacle.getLines()) and (p1, p3) not in lines and (p3, p1) not in lines):
#             return True
#
#         # Check pre-made obstacles inside our triangle
#         pts = obstacle.getPoints()
#
#         center_x = 0
#         center_y = 0
#
#         for (x, y) in pts:
#             center_x += x
#             center_y += y
#
#         center_x /= len(pts)
#         center_y /= len(pts)
#
#         if pointInsidePolygonPoints((center_x, center_y), (p1, p2, p3)):
#             return True
#
#     return False
#
#
#
# def checkCollision3(obstacles, temp1, temp2, agent=None):
#     for obstacle in obstacles:
#         for point in obstacle.getPoints():
#             if minimumDistance((temp1, temp2), point) <= agent.getMaxRadius():
#                 return False
#     return True
#
#
# def midpt(p1, p2):
#     midX = ((p1[0] + p2[0]) / 2)
#     midY = ((p1[1] + p2[1]) / 2)
#     return (midX, midY)
#
#
# def merge(poly1, poly2):
#     pts = []
#     for pt in poly1:
#         pts.append(pt)
#     for pt in poly2:
#         if pt not in pts:
#             pts.append(pt)
#
#     # http://math.stackexchange.com/questions/1329128/
#     # how-to-sort-vertices-of-a-polygon-in-counter-clockwise-order-computing-angle?noredirect=1&lq=1
#     center_x = 0
#     center_y = 0
#
#     for (x, y) in pts:
#         center_x += x
#         center_y += y
#
#     center_x /= len(pts)
#     center_y /= len(pts)
#
#     temp_dict = {}
#     temp_list = []
#
#     for (x, y) in pts:
#         angle = math.atan2(center_y - y, center_x - x)
#         temp_list.append(angle)
#         temp_dict[angle] = (x, y)
#
#     temp_list.sort()
#     pts = []
#     for item in temp_list:
#         pts.append(temp_dict[item])
#
#     return pts
#
#
#
#








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
                    #if not obstructed(point1, point2, world) and not obstructed(point2, point3, world) and not obstructed(point1, point3, world):
                        #lines.append([(point1,point2,point3)])
                        lines.append(((point1[0], point1[1]), (point2[0], point2[1])))

    for l in range(len(lines)):
        x = lines[l][0]
        y = lines[l][1]
        # if rayTraceWorldNoEndPoints(x, y, world.getLines()):
        #     lines[l] = ((0,0), (0,0), (0,0))
        # for o in obstacles:
        #     if pointInsidePolygonLines(x, o.getLines()) and pointInsidePolygonLines(y, o.getLines()):
        #         lines[l] = ((0, 0), (0, 0), (0, 0))
        

    print lines
    triangles = []
    for l in lines:
        print l
        if l not in triangles:
            triangles.append(l)

    polys = triangles

    # for t in range(len(lines)):
    #     for coords in range(len(lines[t])):
    #         x = lines[t][coords][0]
    #         y = lines[t][coords][1]
    #         #if obstructed(x, y, world):
    #         #    lines[t] = [((0, 0), (0, 0), (0, 0))]
    #         if rayTraceWorldNoEndPoints(x, y, world.getLines()):
    #             print lines[t]
    #         for obstacle in obstacles:
    #             if pointInsidePolygonPoints(x, obstacle.getPoints()) and pointInsidePolygonPoints(y,
    #                                                                                                obstacle.getPoints()):
    #                 print lines[t]
    #             if pointInsidePolygonPoints(getMidpoint(x, y), obstacle.getPoints()):
    #                 print lines[t]

    print lines[55]

    # lines.sort()
    # triangles = []
    # for l in lines:
    #     if l not in triangles:
    #         triangles.append(l)
    #
    # edges = lines

    # # for e in range(0, len(lines) - 2, 3):
    # #     triangles.append((lines[e], lines[e + 1], lines[e + 2]))

    # ######## Use triangles to form polygons ########

    for t1 in triangles:
        for t2 in triangles:
            if polygonsAdjacent(t1, t2):
                merged = combinePolys(t1, t2)
                if isConvex(merged) and merged not in polys:
                    polys.append(merged)

    # # ######## Create edges using polygon midpoints ########
    #
    # midpoints = []
    # for p in polys:
    #     for p2 in polys:
    #         point = polygonsAdjacent(p, p2)
    #         if polygonsAdjacent(p, p2):
    #             midpoint = getMidpoint(point[0], point[1])
    #             if midpoint not in midpoints:
    #                 midpoints.append(midpoint)
    # midpoints.sort()
    #
    # for m in range(0, len(midpoints)-1, 2):
    #     if not obstructed(midpoints[m], midpoints[m+1], world):
    #         edges.append((midpoints[m], midpoints[m+1]))
    #
    # ####### Make sure that the edges are agent radius away from each obstacle ########
    #
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
        if pointInsidePolygonPoints(getMidpoint(p1, p2), obstacle.getPoints()):
            return True

    return False

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
