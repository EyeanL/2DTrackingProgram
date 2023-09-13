import cv2, imutils
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from profile import profile
from trackbar import Trackbar
from selector import Selector

class Tracking:

	# Create an instance of the opencv TrackerCSRT Reference Class

	tracker = cv2.TrackerCSRT_create()
	camera = False # False for vid, True for Webcam
	frame_number = 1
	text_font = cv2.FONT_HERSHEY_SIMPLEX

	# Initial Conditions + System Properties

	frame_per_second = 120
	frame_dt = 1 / frame_per_second

	if camera: 
		vid  = cv2.VideoCapture(0)
	else:
		# Access the video file
		vid = cv2.VideoCapture(r"C:\Users\ironi\OneDrive\Documents\stuff\2DTrackingProgram\videos\639 1.mp4")

		# See what these functions do 
		# print(type(vid))
		# print(vid.isOpened())

		number_of_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

	# Read the first frame of the video file use "_," to ignore variable type, ignores the tuple

	_,frame = vid.read()
	frame = imutils.resize(frame,width=1080)
	temp = frame
	cframe = temp 

	# Create a trackbar object

	use = Trackbar()
	use.access_properties(cframe)
	use.coord_system()
	origin = use.get_origin()

	# Create a selector object

	selection = Selector()
	scaler = selection.measurement_selector(frame)

	scaling_factor = scaler
	print(scaling_factor)


	# cv2.selectROI(Window_name, source image) -> top left X, top left Y, width, height
	OBJ = cv2.selectROI(frame, False)
	tracker.init(frame, OBJ)

	# Define the initial conditions
	num_dimensions = 2
	num_parameters = 4 # including time

	time = np.array([0, 0])
	vel = np.array([0, 0])
	acc = np.array([0, 0])

	ang = 0
	angvel = 0
	angacc = 0

	# Create a profile object for the tracked object
	
	obj_profile = profile(scaling_factor, origin, OBJ, time, vel, acc, ang, angvel, angacc)

	mag = obj_profile.find_magnitude()
	starting_ang = np.arctan2(obj_profile.pos[1], obj_profile.pos[0])
	print(starting_ang)

	# Create arrays for each 2-dimensional variable + magnitude and angles for accessibility

	time_arr = time.reshape(1,2)
	pos_arr = obj_profile.pos.reshape(1,2) 
	vel_arr = vel.reshape(1,2)
	acc_arr = acc.reshape(1,2)
	mag_arr = mag.reshape(1,3)
	angles = [starting_ang]

	motion_prof = obj_profile.new_motion
	angsmotion_prof = obj_profile.angs_motion

	# Read through all the frames in the video file until it reaches the last one

	while frame_number < number_of_frames:
		_,frame = vid.read()
		frame = imutils.resize(frame,width = 1080) 

		# Define a boolean 'track_success' that will return true or false if the tracker is able to return a result
		# Then update the tracked frame

		track_success, OBJ = tracker.update(frame)

		# Draw a rectangle for success

		if track_success:
			top_left = (int(OBJ[0]),int(OBJ[1]))
			bottom_right = (int(OBJ[0] + OBJ[2]), int(OBJ[1] + OBJ[3]))
			cv2.rectangle(frame,top_left,bottom_right,(0,0,255),5)

		# Display frame count

		cv2.putText(frame, "Frame Count: " + str(frame_number), (50, 50), text_font, 1, (0, 255, 255), 2, cv2.LINE_4)
		print(frame_number)

		# Update the time accordingly to the fps of the video and take the position of the object

		pos = obj_profile.pos 

		# Take the angle of the object using the arctan2 function then return an angle from 0 to 2pi in orientation of a Cartesian Plane

		cur_ang = np.arctan2(obj_profile.pos[1], obj_profile.pos[0])
		if(cur_ang < 0):
			cur_ang = cur_ang + 2 * np.pi
		angles.append(cur_ang)
		ang = obj_profile.find_angle(angles, angsmotion_prof, frame_number - 1)

		# Run through every frame and use the methods in profile to record the motion profile

		if(frame_number > 1):
			time = obj_profile.update_time(motion_prof, frame_number - 1, frame_dt)
			vel = obj_profile.find_velocity(motion_prof, frame_number - 1, frame_dt)	
			angvel = obj_profile.find_angvelocity(angsmotion_prof, frame_number - 1, frame_dt)	
		else: 
			time = np.array([0, 0])
			vel = np.array([0, 0])
			angvel = 0
	
		if(frame_number > 2):
			acc = obj_profile.find_acceleration(motion_prof, frame_number - 1, frame_dt)
			angacc = obj_profile.find_angacceleration(angsmotion_prof, frame_number - 1, frame_dt)
		else:
			acc = np.array([0, 0])
			angacc = 0

		time_arr = np.append(time_arr, time.reshape(1,2), axis = 0)
		pos_arr = np.append(pos_arr, pos.reshape(1,2), axis = 0)
		vel_arr = np.append(vel_arr, vel.reshape(1,2), axis = 0)
		acc_arr = np.append(acc_arr, acc.reshape(1,2), axis = 0)
	
		obj_profile = profile(scaling_factor, origin, OBJ, time, vel, acc, ang, angvel, angacc)
		mag = obj_profile.find_magnitude()
		mag_arr = np.append(mag_arr, mag.reshape(1,3), axis = 0)
		angs = obj_profile.angs_motion

		angsmotion_prof = np.append(angsmotion_prof, angs, axis = 0)
		motion_prof = np.append(motion_prof, obj_profile.new_motion, axis = 0)
		frame_number = frame_number + 1

		cv2.imshow('Output', frame)

		# Always checking for 'q' key every frame in the while loop to exit whenever

		key  =  cv2.waitKey(1) & 0xff  

		if key == ord('q'):
			frame_number = 1
			break

	vid.release()
	cv2.destroyAllWindows()

	# remove the repeated row used for setting the initial condition

	time_arr = np.delete(time_arr, 0, 0)
	pos_arr = np.delete(pos_arr, 0, 0)
	vel_arr = np.delete(vel_arr, 0, 0)
	acc_arr = np.delete(acc_arr, 0, 0)
	mag_arr = np.delete(mag_arr, 0, 0)
	angsmotion_prof = np.delete(angsmotion_prof, 0, 0)

	# Creating a text file for the data 

	t_data = {
		"time": time_arr[:, 0],
		"x-pos": pos_arr[:, 0],
		"y-pos": pos_arr[:, 1],
		"mag-pos": mag_arr[:, 0],
		"x-vel": vel_arr[:, 0],
		"y-vel": vel_arr[:, 1],
		"mag-vel": mag_arr[:, 1],
		"x-acc": acc_arr[:, 0],
		"y-acc": acc_arr[:, 1],
		"mag-acc": mag_arr[:, 2]
	}
	
	t_df = pd.DataFrame(t_data)
	t_df.to_csv("data_values.csv", sep = '\t', index = False)

	a_data = {
		"time": angsmotion_prof[:, 0],
		"angle": angsmotion_prof[:, 1],
		"ang-vel": angsmotion_prof[:, 2],
		"ang-acc": angsmotion_prof[:, 3]
	}
	
	a_df = pd.DataFrame(a_data)
	a_df.to_csv("angledata_values.csv", sep = '\t', index = False)

	# Plotting the tracked data

	plt.ion()
	plt.figure("Translational Data")

	plt.subplot(3,3,1)
	plt.title('X - Position')
	plt.plot(time_arr[:, 0], pos_arr[:, 0], marker = 'o')

	plt.subplot(3,3,2)
	plt.title('Y - Position')
	plt.plot(time_arr[:, 1], pos_arr[:, 1], marker = 'o')

	plt.subplot(3,3,3)
	plt.title('Position Magnitude')
	plt.plot(time_arr[:, 1], mag_arr[:, 0], marker = 'o')

	plt.subplot(3,3,4)
	plt.title('X - Velocity')
	plt.plot(time_arr[:, 0], vel_arr[:, 0], marker = 'o')

	plt.subplot(3,3,5)
	plt.title('Y - Velocity')
	plt.plot(time_arr[:, 1], vel_arr[:, 1], marker = 'o')

	plt.subplot(3,3,6)
	plt.title('Velocity Magnitude')
	plt.plot(time_arr[:, 1], mag_arr[:, 1], marker = 'o')

	plt.subplot(3,3,7)
	plt.title('X - Acceleration')
	plt.plot(time_arr[:, 0], acc_arr[:, 0], marker = 'o')

	plt.subplot(3,3,8)
	plt.title('Y - Acceleration')
	plt.plot(time_arr[:, 1], acc_arr[:, 1], marker = 'o')

	plt.subplot(3,3,9)
	plt.title('Acceleration Magnitude')
	plt.plot(time_arr[:, 1], mag_arr[:, 2], marker = 'o')

	plt.figure("Angular Data")

	plt.subplot(3,1,1)
	plt.title('Angle')
	plt.plot(angsmotion_prof[:, 0], angsmotion_prof[:, 1], marker = 'o')

	plt.subplot(3,1,2)
	plt.title('Angular Velocity')
	plt.plot(angsmotion_prof[:, 0], angsmotion_prof[:, 2], marker = 'o')

	plt.subplot(3,1,3)
	plt.title('Angular Acceleration')
	plt.plot(angsmotion_prof[:, 0], angsmotion_prof[:, 3], marker = 'o')

	plt.show()
	plt.ginput(1)