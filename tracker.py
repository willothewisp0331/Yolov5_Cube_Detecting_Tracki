import math
import numpy as np


class Tracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0


    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        num_obj = len(objects_rect)
        for rect in objects_rect:
            x, y, w, h, con, b= rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            dist_list = []
            for id, pt in self.center_points.items():
                xx, yy = pt[0]
                n = pt[1]
                dist = math.hypot(cx - xx, cy - yy)
                dist_list.append(dist)

            if len(dist_list) > 1:
                min_dist = np.min(dist_list)
                closest_obj = dist_list.index(min_dist)
            else:
                closest_obj = len(dist_list)
            #
            # print(closest_obj)
            # print(self.center_points)
            for i, key in enumerate(self.center_points.items()):
                if i == closest_obj:
                    id = key[0]
                    n = key[1][1]
                    dist = dist_list[i]
                    if n in [0, 2, 6, 8]: # small cube
                        if dist < 55 and n == b:
                            self.center_points[id] = [(cx, cy), b]
                            objects_bbs_ids.append([x, y, w, h, con, b, id])
                            same_object_detected = True
                            break
                    else:  # big cube
                        if dist < 50 and n == b:
                            self.center_points[id] = [(cx, cy), b]
                            objects_bbs_ids.append([x, y, w, h, con, b, id])
                            same_object_detected = True
                            break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = [(cx, cy), b]
                objects_bbs_ids.append([x, y, w, h, con, b, self.id_count])
                if num_obj == 1:
                    self.id_count = self.id_count
                else:
                    self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids
