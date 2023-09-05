import cv2, imutils
import numpy as np

camera = False # False for vid, True for Webcam
frame_number = 1
text_font = cv2.FONT_HERSHEY_SIMPLEX

#Initial Conditions + System Properties
screen_resolution = (1920, 1080)
frame_per_second = 120
frame_dt = 1 / frame_per_second
frame_width = 1080
fw_scaling = 8

def no_condition(x):
	pass

#The odd_condition does not get updated in the while loop

def odd_condition(x):
	if(cv2.getTrackbarPos('Nbs:' ,'controls') % 2 != 1 or cv2.getTrackbarPos('Nbs:' ,'controls') <= 1):
		nblock_size = cv2.getTrackbarPos('Nbs:' ,'controls') + 1


if camera: 
	vid  = cv2.VideoCapture(0)
else:
	vid = cv2.VideoCapture(r"C:\Users\ironi\OneDrive\Documents\stuff\2DTrackingProgram\videos\balls.mp4")
	number_of_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
	print(number_of_frames)

#use "_," to ignore variable type, ignores the tuple type
_,frame = vid.read()
frame = imutils.resize(frame, frame_width)     
# # cv2.selectROI(Window_name, source image) -> top left X, top left Y, width, height\

gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

OBJ = cv2.selectROI(gray_frame,False)
print(OBJ)
# image[y:y+h, x:x+w] same as an array, rows and cols
frameOI = gray_frame[OBJ[1]: OBJ[1] + OBJ[3], OBJ[0]: OBJ[0] + OBJ[2]]
print(OBJ[2])

h_or_v = 0
cv2.namedWindow('controls', cv2.WINDOW_GUI_NORMAL)
cv2.moveWindow('controls', int(screen_resolution[0] / 2) - int((OBJ[2] * fw_scaling) / 2) , int((OBJ[2] * fw_scaling) / (OBJ[2])) * OBJ[3] + 150)
cv2.resizeWindow('controls', int(OBJ[2] * fw_scaling), 100)
cv2.createTrackbar('Nbs:','controls', 3, 101, odd_condition)
cv2.createTrackbar('Oc:','controls', 0, 100, no_condition)
cv2.createTrackbar('H/W:','controls', 0, 1, no_condition)

while(1):
	nblock_size = cv2.getTrackbarPos('Nbs:' ,'controls')
	offset_constant = cv2.getTrackbarPos('Oc:' ,'controls')
	h_or_v = cv2.getTrackbarPos('H/W:' ,'controls')
	try:
		binary = cv2.adaptiveThreshold(frameOI,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
		cv2.THRESH_BINARY, nblock_size, offset_constant)
	except:
		pass
	binary = imutils.resize(binary, int(OBJ[2] * fw_scaling))
	# contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# cv2.drawContours(binary, contours, -1, (0,255,0), 3)
	dim_bin = binary.shape
	cv2.imshow('Scale the block size and constant then click esc', binary)
	cv2.moveWindow('Scale the block size and constant then click esc', int(screen_resolution[0] / 2) - int(dim_bin[1] / 2), 100)

	key = cv2.waitKey(1) & 0xFF
	if key == 27:
		cv2.destroyAllWindows()
		break 
	
# cv2.imshow('Select a reference measurement by its width', binary)

ref_measurement = cv2.selectROI(binary, False) 
measurement = float(input("Select and Enter a Measurement Value: "))
print(ref_measurement)

# cv2.setWindowTitle('ref_measurement')

if(h_or_v == 0):
	pixeltomeas = measurement / (ref_measurement[2]/fw_scaling)
else:
	pixeltomeas = measurement / (ref_measurement[3]/fw_scaling)

cv2.destroyAllWindows() 
print(pixeltomeas)




# edge_frame = cv2.Canny(frameOI, 30, 200)
# contours, hierarchy = cv2.findContours(edge_frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
# cv2.drawContours(frame, contours, -1, (0,255,0), 3)

#cv2.imshow('first frame', frame)
      
cv2.destroyAllWindows() 

#print(OBJ)