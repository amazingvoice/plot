from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import math

num_of_lanes = int(input("Number of lanes: "))

start_time = time.time()

edge = 2 * num_of_lanes + 1  # edge length of the intersection zone
edge_s = str(edge)

driver = webdriver.Chrome()

# driver.get("https://www.geogebra.org/")
# driver.find_element_by_xpath("//a/span[text()='Start Graphing']").click()

driver.get("https://www.geogebra.org/graphing")
time.sleep(10)  # wait for the page to finish loading

# ==================================================
# ==================== DRAWING =====================
# ==================================================
input_box = driver.find_element_by_id('hiddenCopyPasteLatexArea0')

# ==================================================
# =========== draw intersection boundary ===========
# ==================================================

input_box.send_keys("boundary: Polygon((0, 0), (" + edge_s + ", 0), ("
                    + edge_s + ", " + edge_s + "), (0, " + edge_s + ")")
input_box.send_keys(Keys.RETURN)


# ==================================================
# =============== draw straight lanes ==============
# ==================================================
count = 1
lane_info = {}  # [ (entrance point), (center if any), path_length ]

# N -> S
for i in range(1, num_of_lanes + 1):
    input_box.send_keys("S" + str(count) + ": Segment((" + str(i) + ", " + edge_s + "), (" + str(i) + ", 0))")
    input_box.send_keys(Keys.RETURN)
    lane_info["S" + str(count)] = [(i, edge), edge]
    count += 1

# E -> W
for i in range(0, num_of_lanes):
    input_box.send_keys("S" + str(count) + ": Segment((" + edge_s + ", " + str(2 * num_of_lanes - i) +
                        "), (0, " + str(2 * num_of_lanes - i) + "))")
    input_box.send_keys(Keys.RETURN)
    lane_info["S" + str(count)] = [(edge, 2 * num_of_lanes - i), edge]
    count += 1

# S -> N
for i in range(0, num_of_lanes):
    input_box.send_keys("S" + str(count) + ": Segment((" + str(2 * num_of_lanes - i) +
                        ", 0), (" + str(2 * num_of_lanes - i) + ", " + edge_s + "))")
    input_box.send_keys(Keys.RETURN)
    lane_info["S" + str(count)] = [(2 * num_of_lanes - i, 0), edge]
    count += 1

# W -> E
for i in range(1, num_of_lanes + 1):
    input_box.send_keys("S" + str(count) + ": Segment((0, " + str(i) +
                        "), (" + edge_s + ", " + str(i) + "))")
    input_box.send_keys(Keys.RETURN)
    lane_info["S" + str(count)] = [(0, i), edge]
    count += 1

# ==================================================
# =============== draw turning lanes ===============
# ==================================================

# ==== 1 -- num_of_lanes (R) ====

# center coordinate
x = 0
y = edge

for i in range(1, num_of_lanes + 1):
    input_box.send_keys("R" + str(i) + ": CircularArc((0, " + edge_s + "), (0, " +
                        str(y-i) + "), (" + str(x+i) + ", " + edge_s + "))")
    input_box.send_keys(Keys.RETURN)
    lane_info["R" + str(i)] = [(x + i, edge), (0, edge), math.pi * (x + i) / 2]

# ==== 1 -- num_of_lanes (L) ====

# center coordinate
x = y = edge

for i in range(1, num_of_lanes + 1):
    input_box.send_keys("L" + str(i) + ": CircularArc((" + str(x) + ", " + edge_s +
                        "), (" + str(i) + ", " + edge_s + "), (" + edge_s + ", " + str(i) + "))")
    input_box.send_keys(Keys.RETURN)
    lane_info["L" + str(i)] = [(i, edge), (edge, edge), math.pi * (edge - i) / 2]

# ==== num_of_lanes + 1 -- 2 * num_of_lanes (R) ====

# center coordinate
x = y = edge

for i in range(1, num_of_lanes + 1):
    input_box.send_keys("R" + str(i + num_of_lanes) + ": CircularArc((" + edge_s + ", " + edge_s +
                        "), (" + str(x-i) + ", " + edge_s + "), (" + edge_s + ", " + str(y-i) + "))")
    input_box.send_keys(Keys.RETURN)
    lane_info["R" + str(i + num_of_lanes)] = [(i, edge), (edge, edge), math.pi * (edge - i) / 2]

# ==== num_of_lanes + 1 -- 2 * num_of_lanes (L) ====

# center coordinate
x = edge
y = 0

for i in range(1, num_of_lanes + 1):
    input_box.send_keys("L" + str(i + num_of_lanes) + ": CircularArc((" + edge_s + ", 0), (" +
                        edge_s + ", " + str(edge - i) + "), (" + str(i) + ", 0))")
    input_box.send_keys(Keys.RETURN)
    lane_info["L" + str(i + num_of_lanes)] = [(edge, edge - i), (edge, 0), math.pi * (edge - i) / 2]

# ==== 2 * num_of_lanes + 1 -- 3 * num_of_lanes (R) ====

# center coordinate
x = edge
y = 0

for i in range(1, num_of_lanes + 1):
    input_box.send_keys("R" + str(i + 2 * num_of_lanes) + ": CircularArc((" + edge_s + ", 0), (" +
                        edge_s + ", " + str(i) + "), (" + str(edge - i) + ", 0))")
    input_box.send_keys(Keys.RETURN)
    lane_info["R" + str(i + 2 * num_of_lanes)] = [(edge - i, 0), (edge, 0), math.pi * i / 2]

# ==== 2 * num_of_lanes + 1 -- 3 * num_of_lanes (L) ====

# center coordinate
x = 0
y = 0

for i in range(1, num_of_lanes + 1):
    input_box.send_keys("L" + str(i + 2 * num_of_lanes) + ": CircularArc((0, 0), (" +
                        str(edge - i) + ", 0), (0, " + str(edge - i) + "))")
    input_box.send_keys(Keys.RETURN)
    lane_info["L" + str(i + 2 * num_of_lanes)] = [(edge - i, 0), (0, 0), math.pi * (edge - i) / 2]

# ==== 3 * num_of_lanes + 1 -- 4 * num_of_lanes (R) ====

# center coordinate
x = 0
y = 0

for i in range(1, num_of_lanes + 1):
    input_box.send_keys("R" + str(i + 3 * num_of_lanes) + ": CircularArc((0, 0), (" +
                        str(i) + ", 0), (0, " + str(i) + "))")
    input_box.send_keys(Keys.RETURN)
    lane_info["R" + str(i + 3 * num_of_lanes)] = [(0, i), (0, 0), math.pi * i / 2]

# ==== 3 * num_of_lanes + 1 -- 4 * num_of_lanes (L) ====

# center coordinate
x = 0
y = edge

for i in range(1, num_of_lanes + 1):
    input_box.send_keys("L" + str(i + 3 * num_of_lanes) + ": CircularArc((0, " + edge_s +
                        "), (0, " + str(i) + "), (" + str(edge - i) + ", " + edge_s + "))")
    input_box.send_keys(Keys.RETURN)
    lane_info["L" + str(i + 3 * num_of_lanes)] = [(0, i), (0, edge), math.pi * (edge - i) / 2]


# ===================================================================
# =============== collect collision point coordinates ===============
# ===================================================================

WAIT_TIME = 0.5

SE = []
for i in range(2 * num_of_lanes + 1, 3 * num_of_lanes + 1):
    SE.append("R" + str(i))
for i in range(2 * num_of_lanes, num_of_lanes, -1):
    SE.append("L" + str(i))

SW = []
for i in range(3 * num_of_lanes + 1, 4 * num_of_lanes + 1):
    SW.append("R" + str(i))
for i in range(3 * num_of_lanes, 2 * num_of_lanes, -1):
    SW.append("L" + str(i))

direction = ["S", "R", "L"]
all_lanes = []  # example: "R2"

for l in range(1, num_of_lanes * 4 + 1):
    for d in direction:
        all_lanes.append(d + str(l))

collision_point = {}
combination_map = {}

for i in range(1, num_of_lanes + 1):
    for j in direction:
        for k in all_lanes[(i-1)*3:]:  # (i-1)*3: avoid repeat calculation

            if int(k[1:]) == i:
                continue

            input_box.send_keys("Intersect(" + j + str(i) + ", " + k + ")")
            input_box.send_keys(Keys.RETURN)
            time.sleep(WAIT_TIME)

            res = driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text
            if "=" in res:
                res = res.split(" = ")[1]  # res format: (x, y)

            print(j + str(i) + k + ": " + res)  # PRINT DEBUG INFO

            if "undefined" in res:  # no collision point between these 2 paths
                combination_map[j + str(i) + k] = "undefined"
                continue
            else:  # there is at least one collision point

                temp = res.split(",")
                res_x = float(temp[0][1:])
                res_y = float(temp[1][:len(temp[1]) - 1])

                combination_map[j + str(i) + k] = (res_x, res_y)

                # there are 2 intersection points (symmetric on diagonal 2: y = x)
                if j == "L" and k in SW:

                    if res_x > res_y:
                        swap = res_x
                        res_x = res_y
                        res_y = swap
                        res = str((res_x, res_y))

                    # exchange x and y coordinate
                    res_new = str((res_y, res_x))
                    combination_map[j + str(i) + k] = [(res_x, res_y), (res_y, res_x)]

                    #################################################

                    input_box.send_keys("Angle(" + str(lane_info[j + str(i)][0]) + ", " +
                                        str(lane_info[j + str(i)][1]) + ", " + res + ")")
                    input_box.send_keys(Keys.RETURN)
                    time.sleep(WAIT_TIME)
                    angle = driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text
                    angle = float(angle[:len(angle) - 1])

                    if angle > 90.0:
                        angle = 360 - angle
                    start = angle / 90.0 * lane_info[j + str(i)][2]

                    #################################################

                    input_box.send_keys("Angle(" + str(lane_info[j + str(i)][0]) + ", " +
                                        str(lane_info[j + str(i)][1]) + ", " + res_new + ")")
                    input_box.send_keys(Keys.RETURN)
                    time.sleep(WAIT_TIME)
                    angle = driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text
                    angle = float(angle[:len(angle) - 1])

                    if angle > 90.0:
                        angle = 360 - angle
                    end = angle / 90.0 * lane_info[j + str(i)][2]

                    #################################################

                    collision_point[str(i) + j + k[1:] + k[0]] = [(start, start), (end, end)]
                    continue

                # there are 2 intersection points (symmetric on diagonal 1: y = -x + edge)
                # if j == "R" and k in SE:
                # ***WILL HAPPEN ONLY IF THERE ARE MORE THAN 8 LANES***

                # only 1 intersection point
                # (MAIN PATH) temp as the result: distance from entrance point to the collision point
                if j == "S":  # straight
                    input_box.send_keys("Distance(" + res + ", " + str(lane_info[j + str(i)][0]) + ")")
                    input_box.send_keys(Keys.RETURN)
                    time.sleep(WAIT_TIME)
                    temp = float(driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text)
                else:  # turning
                    input_box.send_keys("Angle(" + res + ", " +
                                        str(lane_info[j + str(i)][1]) + ", " + str(lane_info[j + str(i)][0]) + ")")
                    input_box.send_keys(Keys.RETURN)
                    time.sleep(WAIT_TIME)
                    temp = driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text
                    temp = float(temp[:len(temp) - 1])

                    if temp > 90.0:
                        temp = 360 - temp
                    temp = temp / 90.0 * lane_info[j + str(i)][2]

                # temp2 as the result: distance from entrance point to the collision point
                if "S" in k:
                    input_box.send_keys("Distance(" + res + ", " + str(lane_info[k][0]) + ")")
                    input_box.send_keys(Keys.RETURN)
                    time.sleep(WAIT_TIME)
                    temp2 = float(driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text)
                else:
                    input_box.send_keys("Angle(" + res + ", " +
                                        str(lane_info[k][1]) + ", " + str(lane_info[k][0]) + ")")
                    input_box.send_keys(Keys.RETURN)
                    time.sleep(WAIT_TIME)
                    temp2 = driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text
                    temp2 = float(temp2[:len(temp2) - 1])
                    if temp2 > 90.0:
                        temp2 = 360 - temp2
                    temp2 = temp2 / 90.0 * lane_info[k][2]

                collision_point[str(i) + j + k[1:] + k[0]] = (temp2, temp)


# ============================================================================
# =================  find places where near-miss may happen  =================
# ============================================================================

safe_distance = 1.0

# 1 - num_of_lanes (L)
for i in range(1, num_of_lanes + 1):
    for j in reversed(SW):

        temp = combination_map["L" + str(i) + j]
        # first near-miss path found
        if temp == "undefined":

            print("first undefined: L" + str(i) + j)

            center_old = lane_info["L" + str(i)][1]
            center_new = (center_old[0] - safe_distance / math.sqrt(2.0),
                          center_old[1] - safe_distance / math.sqrt(2.0))
            entrance_old = lane_info["L" + str(i)][0]
            entrance_new = (entrance_old[0] - safe_distance / math.sqrt(2.0),
                            entrance_old[1] - safe_distance / math.sqrt(2.0))
            exit_old = (entrance_old[1], entrance_old[0])
            exit_new = (exit_old[0] - safe_distance / math.sqrt(2.0),
                        exit_old[1] - safe_distance / math.sqrt(2.0))
            # draw moved path
            input_box.send_keys("L" + str(i) + "new: CircularArc(" + str(center_new) +
                                ", " + str(entrance_new) + ", " + str(exit_new) + ")")
            input_box.send_keys(Keys.RETURN)
            time.sleep(WAIT_TIME)

            # get new intersection points
            input_box.send_keys("Intersect(L" + str(i) + "new, " + j + ")")
            input_box.send_keys(Keys.RETURN)
            time.sleep(WAIT_TIME)
            res = driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text

            if "=" in res:  # there are 2 intersection points
                print("res: " + res)
                print("Moved path have 2 intersections.")
                temp = res.split(" = ")[1]
                temp = temp.split(",")

                # make sure x <= y
                res_x = float(temp[0][1:])
                res_y = float(temp[1][:len(temp[1]) - 1])
                if res_x > res_y:
                    swap = res_x
                    res_x = res_y
                    res_y = swap
                    res = str((res_x, res_y))

                input_box.send_keys("Angle(" + str(entrance_new) +
                                    ", " + str(center_new) + ", " + res + ")")
                input_box.send_keys(Keys.RETURN)
                time.sleep(WAIT_TIME)
                angle = driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text
                angle = float(angle[:len(angle) - 1])

                if angle > 90.0:
                    angle = 360 - angle
                # start
                start = angle / 90.0 * lane_info["L" + str(i)][2]

                # exchange x and y coordinate
                res_new = str((res_y, res_x))

                input_box.send_keys("Angle(" + str(entrance_new) + ", " +
                                    str(center_new) + ", " + res_new + ")")
                input_box.send_keys(Keys.RETURN)
                time.sleep(WAIT_TIME)
                angle = driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text
                angle = float(angle[:len(angle) - 1])

                if angle > 90.0:
                    angle = 360 - angle
                # end
                end = angle / 90.0 * lane_info["L" + str(i)][2]

                # ===== calculate coordinates for j =====
                input_box.send_keys("Angle(" + str(lane_info[j][0]) +
                                    ", " + str(lane_info[j][1]) + ", " + res + ")")
                input_box.send_keys(Keys.RETURN)
                time.sleep(WAIT_TIME)
                angle = driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text
                angle = float(angle[:len(angle) - 1])

                if angle > 90.0:
                    angle = 360 - angle
                # start
                start2 = angle / 90.0 * lane_info[j][2]

                input_box.send_keys("Angle(" + str(lane_info[j][0]) + ", " +
                                    str(lane_info[j][1]) + ", " + res_new + ")")
                input_box.send_keys(Keys.RETURN)
                time.sleep(WAIT_TIME)
                angle = driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text
                angle = float(angle[:len(angle) - 1])

                if angle > 90.0:
                    angle = 360 - angle
                # end
                end2 = angle / 90.0 * lane_info[j][2]

                if start2 > end2:
                    swap = start2
                    start2 = end2
                    end2 = swap

                collision_point[str(i) + "L" + j[1:] + j[0]] = [(start2, start), (end2, end)]
            break

# 1 - num_of_lanes (R)
for i in range(1, num_of_lanes + 1):
    for j in reversed(SE):

        temp = combination_map["R" + str(i) + j]

        # first near-miss path found
        if temp == "undefined":

            print("first undefined: R" + str(i) + j)

            center_old = lane_info["R" + str(i)][1]
            center_new = (center_old[0] + safe_distance / math.sqrt(2.0),
                          center_old[1] - safe_distance / math.sqrt(2.0))

            entrance_old = lane_info["R" + str(i)][0]
            entrance_new = (entrance_old[0] + safe_distance / math.sqrt(2.0),
                            entrance_old[1] - safe_distance / math.sqrt(2.0))

            exit_old = (edge - entrance_old[1], edge - entrance_old[0])
            exit_new = (exit_old[0] + safe_distance / math.sqrt(2.0),
                        exit_old[1] - safe_distance / math.sqrt(2.0))

            # draw moved path
            input_box.send_keys("R" + str(i) + "new: CircularArc(" + str(center_new) +
                                ", " + str(exit_new) + ", " + str(entrance_new) + ")")
            input_box.send_keys(Keys.RETURN)
            time.sleep(WAIT_TIME)

            # get new intersection points
            input_box.send_keys("Intersect(R" + str(i) + "new, " + j + ")")
            input_box.send_keys(Keys.RETURN)
            time.sleep(WAIT_TIME)
            res = driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text

            if "=" in res:  # there are 2 intersection points
                temp = res.split(" = ")[1]
                temp = temp.split(",")

                res_x = float(temp[0][1:])
                res_y = float(temp[1][:len(temp[1]) - 1])

                # 2 intersection points
                res = str((res_x, res_y))
                res_new = str((edge - res_y, edge - res_x))

                input_box.send_keys("Angle(" + str(entrance_new) +
                                    ", " + str(center_new) + ", " + res + ")")
                input_box.send_keys(Keys.RETURN)
                time.sleep(WAIT_TIME)
                angle = driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text
                angle = float(angle[:len(angle) - 1])

                if angle > 90.0:
                    angle = 360 - angle
                # start
                start = angle / 90.0 * lane_info["R" + str(i)][2]
                #########
                input_box.send_keys("Angle(" + str(entrance_new) + ", " +
                                    str(center_new) + ", " + res_new + ")")
                input_box.send_keys(Keys.RETURN)
                time.sleep(WAIT_TIME)
                angle = driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text
                angle = float(angle[:len(angle) - 1])

                if angle > 90.0:
                    angle = 360 - angle
                # end
                end = angle / 90.0 * lane_info["R" + str(i)][2]

                # make sure start <== end
                if start > end:
                    swap = start
                    start = end
                    end = swap

                # ===== calculate coordinates for j =====
                input_box.send_keys("Angle(" + str(lane_info[j][0]) +
                                    ", " + str(lane_info[j][1]) + ", " + res + ")")
                input_box.send_keys(Keys.RETURN)
                time.sleep(WAIT_TIME)
                angle = driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text
                angle = float(angle[:len(angle) - 1])

                if angle > 90.0:
                    angle = 360 - angle
                # start
                start2 = angle / 90.0 * lane_info[j][2]

                input_box.send_keys("Angle(" + str(lane_info[j][0]) + ", " +
                                    str(lane_info[j][1]) + ", " + res_new + ")")
                input_box.send_keys(Keys.RETURN)
                time.sleep(WAIT_TIME)
                angle = driver.find_element_by_xpath("(//div[@class='gwt-HTML'])[last()]").text
                angle = float(angle[:len(angle) - 1])

                if angle > 90.0:
                    angle = 360 - angle
                # end
                end2 = angle / 90.0 * lane_info[j][2]

                # make sure start <= end
                if start2 > end2:
                    swap = start2
                    start2 = end2
                    end2 = swap

                collision_point[str(i) + "R" + j[1:] + j[0]] = [(start2, start), (end2, end)]
            break
# =======================================================================================

f = open("collision_point.txt", "a")
f.seek(0)
f.truncate()

for item in collision_point:
    print(item, collision_point[item])
    f.write(item + ": " + str(collision_point[item]) + "\n")

# driver.close()

end_time = time.time()

# program timer
print("time elapsed: " + str(end_time - start_time) + "s")
f.write("time elapsed: " + str(end_time - start_time) + "s\n")
f.close()
