from profile import profile
import numpy as np

class test:
    # time = np.array([1, 1])
    # vel = np.array([1, 1])
    # acc = np.array([1, 1])
    # print(time)
    ROIStats = [300, 300, 50, 50]
    # obj_profile = profile(ROIStats, time, vel, acc)
    # obj_profile.append_motion()
    # print(obj_profile.get_motion_profile())
    # new_obj_profile = profile(ROIStats, time, vel, acc)
    # new_obj_profile.append_motion()
    # print(new_obj_profile.get_motion_profile())
    OBJ = np.array([2,1])
    print(OBJ)

    dt = 0.5

    time = np.array([[0, 0]])
    vel = np.array([0, 0])
    acc = np.array([0, 0])
    num_dimensions = 2
    num_parameters = 4 # including time
    #motion_prof = profile(ROIStats, time, vel, acc)
    # print(motion_prof[0, 0, :] + dt)
    # print(motion_prof.get_new_motion())
    # motion_prof.update_time(motion_prof.new_motion, frame_number = 0, dt = 0.15)
    # print(motion_prof.new_motion)
    # new_motion_prof = profile(ROIStats, time, vel, acc)
    # newst = np.append(motion_prof.new_motion, new_motion_prof.new_motion, axis = 0)
    # stewn = profile(ROIStats, time, vel, acc)
    # print(np.append(newst, stewn.new_motion, axis = 0))
    print(time)
    print(np.shape(vel))
    print(vel.reshape(1,2))
    print(np.append(time, vel))