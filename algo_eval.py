#!/usr/bin/env python

import os
import json
from pprint import pprint
from threading import Thread
import time

def run_eval(algorithm, resize_factor, alpha, mvt_tolerance, smooth_filter, smooth_filt_size, max_detectable_distance, min_obj_height, obj_ratio, \
post_filter, post_filt_size, merge_algo, merge_margin, bg_er_thresh, bg_dl_thresh):

    run_counter = 0
    total_runs = len(algorithm) * len(resize_factor) * len(alpha) * len(mvt_tolerance) * len(smooth_filter) * len(smooth_filt_size) * \
    len(max_detectable_distance) * len(min_obj_height) * len(obj_ratio) * len(post_filter) * len(post_filt_size) * len(merge_algo) * \
    len(merge_margin) * len(bg_er_thresh) * len(bg_dl_thresh)

    for algo in algorithm:
        data["plugins"]["motion_detection"]["algorithm"] = algo
        for rsz in resize_factor:
            data["plugins"]["motion_detection"]["configuration"]["resize_factor"] = rsz
            for a in alpha:
                data["plugins"]["motion_detection"]["configuration"]["alpha"] = a
                for max_dist in max_detectable_distance:
                    data["plugins"]["motion_detection"]["configuration"]["max_detectable_distance"] = max_dist
                    for sm_sz in smooth_filt_size:
                        data["plugins"]["motion_detection"]["configuration"]["smooth_filt_size"] = sm_sz
                        for ps_sz in post_filt_size:
                            data["plugins"]["motion_detection"]["configuration"]["post_filt_size"] = ps_sz
                            for thresh in bg_er_thresh:
                                data["plugins"]["motion_detection"]["configuration"][algo]["bg_er_thresh"] = thresh

                                editted_file = open(conf_path + "ECV.json", "w")
                                json.dump(data, editted_file, indent=4, sort_keys=True)
                                editted_file.close()
                                run_counter += 1
                                print("Running test " + str(run_counter) + "/" + str(total_runs) + "...")
                                os.system(eval_path + "ecv_algo_eval " + conf_path + "ECV_tools.json")


base_path = "/home/tanman/work/dev/dcim/cctv/cctv-server/"
eval_path = base_path + "build-release/tests/"
conf_path = base_path + "deployment/conf/"
data = []

with open(conf_path + "ECV_base.json", "r") as data_file:
    text = data_file.read()
    data = json.loads(text)

algorithm = ["adaptive_average"]
resize_factor = [2, 3]
alpha = [0.05, 0.1, 0.2]
mvt_tolerance = [0]
smooth_filter = [1]
smooth_filt_size =[7, 15]
max_detectable_distance = [10, 25, 50]
min_obj_height = [1.6]
obj_ratio = [0.41]
post_filter = [1]
post_filt_size = [7, 15]
merge_algo = [1]
merge_margin = [0.1]
bg_er_thresh = [5, 15, 30]

for t in bg_er_thresh:
    t = Thread(target=run_eval, args=(algorithm, resize_factor, alpha, mvt_tolerance, smooth_filter, smooth_filt_size, max_detectable_distance, \
    min_obj_height, obj_ratio, post_filter, post_filt_size, merge_algo, merge_margin, [t], bg_dl_thresh,))
    print("starting thread with bg_er_thresh=" + str(t))
    t.start()
    time.sleep(10)
