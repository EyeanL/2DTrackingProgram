import numpy as np
import matplotlib as plt

class profile(object):

    # Define the number of dimensions and parameters that will be tracked for the object

    num_dimensions = 2
    num_parameters = 4 # including time

    # motion_prof for 2 dimensional variables

    motion_prof = np.zeros([1, num_parameters, num_dimensions], float)

    def __init__(self, scaling_factor, origin, ROIStats, time, vel, acc, ang, angvel, angacc):

        # Obtain ROIStats in the format of cv2.selectROI(Window_name, source image) -> top left X, top left Y, width, height
        # Then convert them into useful variables and store them into motion profile arrays 

        tl_x = ROIStats[0] - origin[0]
        tl_y = ROIStats[1] - origin[1]
        width = ROIStats[2] 
        height = ROIStats[3]

        self.size = np.array([width, height])

        # Obtain the center position of the object from the ROIStats

        self.pos = np.array([tl_x + (width / 2), tl_y + (height / 2)], dtype = float) * scaling_factor
        self.vel = vel
        self.acc = acc

        # Create arrays to store the motion profile data
        # Create seperate arrays for variables with different amount of dimensions

        self.new_motion = np.array([time, self.pos, vel, acc], dtype = float).reshape(1, self.num_parameters, self.num_dimensions)
        self.angs_motion = np.array([time[0], ang, angvel, angacc], dtype = float).reshape(1, self.num_parameters)

    def append_motion(self):
        self.motion_prof = np.append(self.motion_prof, self.new_motion, axis = 0)

    # Update the time of the motion given previous time + dt

    def update_time(self, motion_prof, frame_number, dt):
        return motion_prof[frame_number, 0, :] + dt

    # Update the velocity of the motion given previous change in position / change in time

    def find_velocity(self, motion_prof, frame_number, dt: float):
        return (motion_prof[frame_number, 1, :] - motion_prof[frame_number - 1, 1, :]) / dt
    
    # Update the velocity of the motion given previous change in velocity / change in time

    def find_acceleration(self, motion_prof, frame_number, dt: float):
        return (motion_prof[frame_number, 2, :] - motion_prof[frame_number - 1, 2, :]) / dt
    
    # Calculate the angle of the object with respect to the cartesian plane 
    
    def find_angle(self, angles, angsmotion_prof, frame_number):
        #find the angle difference between the current and previous frame
        res_angle = angles[frame_number] - angles[frame_number - 1]
        #check for angle wrap arounds and adjust accordingly
        if(res_angle > np.pi):
            res_angle = res_angle - (2 * np.pi)
        elif(res_angle < (-1 * np.pi)):
            res_angle = res_angle + (2 * np.pi)

        return angsmotion_prof[frame_number, 1] + res_angle

    # Find the respective time dervatives for the angle in the same way as position

    def find_angvelocity(self, angsmotion_prof, frame_number, dt: float):
        return (angsmotion_prof[frame_number, 1] - angsmotion_prof[frame_number - 1, 1]) / dt
    
    def find_angacceleration(self, angsmotion_prof, frame_number, dt: float):
        return (angsmotion_prof[frame_number, 2] - angsmotion_prof[frame_number - 1, 2]) / dt
    
    # Calculate the magnitude of the position and time derivatives with the x and y components.

    def find_magnitude(self):
        pos_mag = np.sqrt(self.pos[0] ** 2 + self.pos[1] ** 2)
        vel_mag = np.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)
        acc_mag = np.sqrt(self.acc[0] ** 2 + self.acc[1] ** 2)
        return np.array([pos_mag, vel_mag, acc_mag])

    def get_motion_profile(self):
        return self.motion_prof
    
    def get_new_motion(self):
        return self.new_motion
    
    # for a practice, create method in the profile class to plot and write the motion profiles to be called in the main class for organization

    def plot_motion_profile(self, motion_prof, frame_number):
        pass

    def write_motion_profile(self, motion_prof, frame_number):
        pass

        
    

