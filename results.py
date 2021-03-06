#!/usr/bin/env python

import os
from pprint import pprint
import matplotlib.pyplot as plt
import json
import numpy as np


#  User Input
# ***********
results_path = "/home/tanman/work/dev/test_samples/eval"
#  Select here the parameter to be used for clustering in color/marker
#  can be one of {resize_factor, max_detectable_distance, alpha, smooth_filt_size, post_filt_size , bg_er_thresh}:
color_cluster = "max_detectable_distance"
marker_cluster = "resize_factor"
#  Color and marker palette
colors = ["r", "g", "b", "k"]
markers = ["o", "s", "*", "^"]


#  Variables Declaration
# **********************
folders = []
Frames = []
TP = []
TN = []
FP = []
FN = []
HR = []
FPR = []
Acc = []
Pre = []
F1 = []
Runtime = []
rsz = []
alpha = []
dist = []
sm_sz = []
post_sz = []
thresh = []
legends = []
cluster = {}
cluster["resize_factor"] = rsz
cluster["max_detectable_distance"] = dist
cluster["alpha"] = alpha
cluster["smooth_filt_size"] = sm_sz
cluster["post_filt_size"] = post_sz
cluster["bg_er_thresh"] = thresh


#  Parse results
# **************
for root, dirs, files in os.walk(results_path):
    dirs.sort()
    if len(files) >= 3:  #  we expect to have at least 3 files: ECV.json, ECV_tools.json and eval_motion_detection.txt
        folders.append(os.path.split(root)[-1])
        for filename in files:
            if filename == "eval_motion_detection.txt": #  parse results file
                with open(os.path.join(root, filename), "r") as res_file:
                    for line in res_file:
                        line = line.strip()
                        metrics = line.split(": ")
                        if len(metrics) < 2:  # line without metrics or wrong format (should be "metric_name: metric_value")
                            break
                        key = metrics[0]
                        val = metrics[1]
                        if key == "Frames":
                            Frames.append(int(val))
                        elif key == "TP":
                            TP.append(val)
                        elif key == "TN":
                            TN.append(val)
                        elif key == "FP":
                            FP.append(val)
                        elif key == "FN":
                            FN.append(val)
                        elif key == "HR":
                            float_val = float(val[:-1])/100.0
                            HR.append(float_val)
                        elif key == "FPR":
                            float_val = float(val[:-1])/100.0
                            FPR.append(float_val)
                        elif key == "Acc":
                            float_val = float(val[:-1])/100.0
                            Acc.append(float_val)
                        elif key == "Pre":
                            float_val = float(val[:-1])/100.0
                            Pre.append(float_val)
                        elif key == "F1":
                            float_val = float(val[:-1])/100.0
                            F1.append(float_val)
                        elif key == "Runtime":
                            Runtime.append(int(val))
                        else:
                            print("Could not understand metric, skipping line: \'" + line + "\' in folder \'" + folders[-1] + "\'")
            
            elif filename == "ECV.json":  #  parse configuration file and save parameter values
                with open(os.path.join(root, filename), "r") as ecv_file:
                    text = ecv_file.read()
                    data = json.loads(text)
                    algo = data["plugins"]["motion_detection"]["algorithm"]
                    rsz.append(data["plugins"]["motion_detection"]["configuration"]["resize_factor"])
                    alpha.append(data["plugins"]["motion_detection"]["configuration"]["alpha"])
                    dist.append(data["plugins"]["motion_detection"]["configuration"]["max_detectable_distance"])
                    sm_sz.append(data["plugins"]["motion_detection"]["configuration"]["smooth_filt_size"])
                    post_sz.append(data["plugins"]["motion_detection"]["configuration"]["post_filt_size"])
                    thresh.append(data["plugins"]["motion_detection"]["configuration"][algo]["bg_er_thresh"])
            
            #  Make sure FPR and HR have same dimension
            if len(HR) > len(FPR):
                del HR[-1]
            if len(FPR) > len(HR):
                del FPR[-1]


#  Process and plot the results
# *****************************
x = np.array(FPR)
y = np.array(HR)
rt_array = np.array(Runtime)
fr_array = np.array(Frames)
fps = np.round(fr_array / rt_array)

color_mask = np.array(cluster[color_cluster])
marker_mask = np.array(cluster[marker_cluster])
size_mask = fps

for i, col_val in enumerate(sorted(set(color_mask))):
    xc = x[color_mask == col_val]
    yc = y[color_mask == col_val]
    color_marker_mask = marker_mask[color_mask == col_val]
    size = size_mask[color_mask == col_val]
    c = colors[i%len(colors)]
    for j, mark_val in enumerate(sorted(set(marker_mask))):
        xcm = xc[color_marker_mask == mark_val]
        ycm = yc[color_marker_mask == mark_val]
        s = size[color_marker_mask == mark_val]
        m = markers[j%len(markers)]
        plt.scatter(xcm, ycm, s=16*(s-min(fps))+20, marker=m, c=c, alpha=0.5, label=color_cluster+"="+str(col_val)+", "+marker_cluster+"="+str(mark_val))
        
plt.legend(loc='lower right')
plt.title("ROC curve (" + str(len(HR)) + " tests)")
plt.xlabel("FPR (%)")
plt.ylabel("HR (%)")
plt.grid(True)
plt.axis([0, plt.xlim()[1], 0, 1])

#~ for x_, y_, fps_ in np.broadcast(x, y, fps):
    #~ plt.annotate(fps_, (x_,y_))

plt.show()
