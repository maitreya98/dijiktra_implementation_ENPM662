import numpy as np
import cv2
from mapping import *


class Node:
    def __init__(self, point):
        self.point = point
        self.cost = None
        self.parent = None


class point_robot:
    def __init__(self, dim, clear, int_pos, final_pos):
        self.dim = dim
        self.clear = clear
        self.int_pos = int_pos
        self.final_pos = final_pos


def priorityqueue(queue):  # Priority Queue, result of this are the least cost nodes 
    val = 0
    for i in range(len(queue)):
        if queue[i].cost < queue[val].cost:
            val = i
    return queue.pop(val)


def findNode(point, queue):
    for i in queue:
        if i.point == point:
            return queue.index(i)
        else:
            return None


def move_up(point, dim, tol, points_updated):
    point_x = point[0]
    point_y = point[1]
    cost = 1
    if point_y > 0 and not (obst_flag(point, dim, tol, points_updated)):
        new_point = [point_x, point_y - 1]
        return new_point, cost
    else:
        return None, None


def move_down(point, dim, tol, points_updated):
    point_x = point[0]
    point_y = point[1]
    cost = 1
    if point_y < 250 and not (obst_flag(point, dim, tol, points_updated)):
        new_point = [point_x, point_y + 1]
        return new_point, cost
    else:
        return None, None


def move_left(point, dim, tol, points_updated):
    point_x = point[0]
    point_y = point[1]
    cost = 1
    if point_x > 0 and not (obst_flag(point, dim, tol, points_updated)):
        new_point = [point_x - 1, point_y]
        return new_point, cost
    else:
        return None, None


def move_right(point, dim, tol, points_updated):
    point_x = point[0]
    point_y = point[1]
    cost = 1
    if point_x < 400 and not (obst_flag(point, dim, tol, points_updated)):
        new_point = [point_x + 1, point_y]
        return new_point, cost
    else:
        return None, None


def move_up_right(point, dim, tol, points_updated):
    point_x = point[0]
    point_y = point[1]
    cost = np.sqrt(2)
    if point_x < 400 and point_y > 0 and not (obst_flag(point, dim, tol, points_updated)):
        new_point = [point_x + 1, point_y - 1]
        return new_point, cost
    else:
        return None, None


def move_up_left(point, dim, tol, points_updated):
    point_x = point[0]
    point_y = point[1]
    cost = np.sqrt(2)
    if point_x > 0 and point_y > 0 and not (obst_flag(point, dim, tol, points_updated)):
        new_point = [point_x - 1, point_y - 1]
        return new_point, cost
    else:
        return None, None


def move_down_right(point, dim, tol, points_updated):
    point_x = point[0]
    point_y = point[1]
    cost = np.sqrt(2)
    if point_x < 400 and point_y < 250 and not (obst_flag(point, dim, tol, points_updated)):
        new_point = [point_x + 1, point_y + 1]
        return new_point, cost
    else:
        return None, None


def move_down_left(point, dim, tol, points_updated):
    point_x = point[0]
    point_y = point[1]
    cost = np.sqrt(2)
    if point_x > 0 and point_y < 250 and not (obst_flag(point, dim, tol, points_updated)):
        new_point = [point_x - 1, point_y + 1]
        return new_point, cost
    else:
        return None, None


def fetch_node(action, current_point, dim, tol, points_updated):
    if action == 'up':
        return move_up(current_point, dim, tol, points_updated)
    if action == 'down':
        return move_down(current_point, dim, tol, points_updated)
    if action == 'left':
        return move_left(current_point, dim, tol, points_updated)
    if action == 'right':
        return move_right(current_point, dim, tol, points_updated)
    if action == 'up_right':
        return move_up_right(current_point, dim, tol, points_updated)
    if action == 'up_left':
        return move_up_left(current_point, dim, tol, points_updated)
    if action == 'down_right':
        return move_down_right(current_point, dim, tol, points_updated)
    if action == 'down_left':
        return move_down_left(current_point, dim, tol, points_updated)


def start_pts(point):
    point_x = point[0]
    point_y = point[1]
    count = 0
    if point_y > 0:
        count += 1
    if point_y < 250:
        count += 1
    if point_x > 0:
        count += 1
    if point_x < 400:
        count += 1
    if point_x < 400 and point_y > 0:
        count += 1
    if point_x > 0 and point_y > 0:
        count += 1
    if point_x < 400 and point_y < 250:
        count += 1
    if point_x > 0 and point_y < 250:
        count += 1
    print("count :", count)
    return count


def color_the_map(image_color, point):
    image_color[point[1], point[0]] = [255, 255, 255]
    return image_color


def backtracking(node):
    print("Back-Tracking the Visited Nodes")
    p = list()
    p.append(node.parent)
    parent = node.parent
    if parent is None:
        return p
    while parent is not None:
        p.append(parent)
        parent = parent.parent
    pts_rev = list(p)
    return pts_rev


def Djikstra(image, point_robot, resolution):
    dim = point_robot.dim
    tol = point_robot.clear
    start_node_pos = point_robot.int_pos
    goal_node_pos = point_robot.final_pos

    image[start_node_pos[1], start_node_pos[0]] = [255, 0, 213]
    image[goal_node_pos[1], goal_node_pos[0]] = [0, 0, 139]
    start_node = Node(start_node_pos)
    start_node.cost = 0

    entry_points = start_pts(goal_node_pos)
    print("Entry points", entry_points)
    visited = list()
    queue = [start_node]
    actions = ["up", "down", "left", "right", "up_right", "down_right", "up_left", "down_left"]
    counter = 0

    while queue:
        current_node = priorityqueue(queue)
        current_point = current_node.point
        visited.append(str(current_point))

        if counter == entry_points:
            return new_node.parent, image

        for action in actions:
            new_point, base_cost = fetch_node(action, current_point, dim, tol,points_updated)
            if new_point is not None:
                if new_point == goal_node_pos:
                    if counter < entry_points:
                        counter += 1
                        print("Goal Reached. ", counter)

                new_node = Node(new_point)
                new_node.parent = current_node

                image = color_the_map(image, current_node.point)
                image[start_node_pos[1], start_node_pos[0]] = [255, 0, 213]
                image[goal_node_pos[1], goal_node_pos[0]] = [0, 0, 139]

                resized_new_1 = cv2.resize(image, None, fx=resolution, fy=resolution, interpolation=cv2.INTER_CUBIC)
                cv2.imshow("Display", resized_new_1)
                cv2.waitKey(1)

                if str(new_point) not in visited:
                    new_node.cost = base_cost + new_node.parent.cost
                    visited.append(str(new_node.point))
                    queue.append(new_node)
                else:
                    node_exist_index = findNode(new_point, queue)
                    if node_exist_index is not None:
                        temp_node = queue[node_exist_index]
                        if temp_node.cost > base_cost + new_node.parent.cost:
                            temp_node.cost = base_cost + new_node.parent.cost
                            temp_node.parent = current_node
            else:
                continue
    return None, None



# User Inputs for a start point and end point (for which short distance will be calculated)
print("This is a practical implementation of Djikstra's Algorithm using a point robot module !")
start_cords_x = int(input("start x-coordinate: "))
start_cords_y = int(input("start y-coordinate: "))
goal_cords_x = int(input("goal x-coordinate: "))
goal_cords_y = int(input("goal y-coordinate: "))

# Here dimension and clearance will be 0 , initially
dim = 0
tol = 0

start_cords_y = 250 - start_cords_y
goal_cords_y = 250 - goal_cords_y


if start_cords_x > 400 or goal_cords_x > 400:
    print("The x coordinate should be within the range of [0-400]")
    exit(0)

if start_cords_y > 250 or goal_cords_y > 250:
    print("The y coordinate should be within the range of [0-250]")
    exit(0)

start_node_position = [start_cords_x, start_cords_y]
goal_node_position = [goal_cords_x, goal_cords_y]

robo = point_robot(dim, tol, start_node_position, goal_node_position)

points_updated = hexa_points(robo.dim, robo.clear)
image_int = plot_image(points_updated, robo.dim, robo.clear)

if obst_flag(start_node_position, robo.dim, robo.clear, points_updated):
    print("Error: The initial point is in the obstacle!")
    exit(0)

if obst_flag(goal_node_position, robo.dim, robo.clear, points_updated):
    print("Error: The goal point is in the obstacle!")
    exit(0)

result, image = Djikstra(image_int, robo, 2)

if result is not None:
    nl = backtracking(result)
    for i in nl:
        x = i.point[1]
        y = i.point[0]
        image[x, y] = [255, 0 , 0]
        resized_new = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        cv2.imshow("Fig", resized_new)
        cv2.waitKey(100)
else:
    print("Sorry, Result not achieved !")

print("Tap to Quit")


cv2.waitKey(0)
cv2.destroyAllWindows()