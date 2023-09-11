# 2DTrackingProgram

<!-----

Yay, no errors, warnings, or alerts!

Conversion time: 0.59 seconds.


Using this Markdown file:

1. Paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β34
* Mon Sep 11 2023 08:40:01 GMT-0700 (PDT)
* Source doc: 2D GUI Object Tracking Software Documentation / Training Manual
* This is a partial selection. Check to make sure intra-doc links work.
----->



#### Program Set Up



1. Have python installed + a python IDE and install the required libraries (numpy, opencv, and matplotlib)

Run the following commands in the terminal:
  * pip install numpy
  * pip install opencv-contrib-python
  * pip install matplotlib
2. The code to the program can be found on this github repository: [https://github.com/EyeanL/2DTrackingProgram](https://github.com/EyeanL/2DTrackingProgram) 

To run programs from ang github repositories follow this guide for vscode:  

[https://www.youtube.com/watch?v=XKWh3C3B1uA&ab_channel=RethinkingUI](https://www.youtube.com/watch?v=XKWh3C3B1uA&ab_channel=RethinkingUI) 



3. In the same folder for the code files, create another inside that will contain the videos to be tracked. The better quality and fps the video is, the better the resolution of the tracking will be.
* To access the video make sure to change the directory in line 28, and change the reference directory accordingly to file location -> videos folder -> video file.
4. The program setup is now complete and the user is now able to begin using the program!


#### Program Instructions Manual



1. Run all the files in the folder, then run the main file (tracking.py)
2. Enter the standard variables, such as the FPS and resolution of the video that was taken and in lines 20-21 and selector.py line 19.
3. Once tracking.py has been run the first frame of the video will be shown, prompting the user to define a coordinate system.
* Click any point on the first frame of the video and an origin located at where the user clicked on the frame with an x and y axis will be shown on the frame. 
* Readjust the origin of the coordinate system until the user is satisfied then click the “enter” key to continue.
4. Next, the frame will prompt the user to select a region of interest to select a measurement point for reference (usually a measuring apparatus or an object that is on the same plane as the object of interest projected onto from the camera) to which the user can click and drag across the frame, creating a rectangle.
* After selecting the region of interest, containing the reference measurement, another frame will pop up to which the user will be able to adjust the min and max values of the neighboring contrast block size (from 3 to 101 in step sizes of 2) and mean subtraction constant (from 0 to 100) until a clear result can be seen to determine an area of selection. The user will also have the option to choose a horizontal or vertical line of reference. (from 0 to 1, 0 for horizontal and 1 for vertical).
* Once satisfied with the clarity of the binary image and orientation for the line of reference, click enter and the user will be prompted to select a rectangle as for a reference measurement. Either the width or height of the rectange will be used as the line of reference depending on the orientation chosen by the user. 
* Once the line of reference has been chosen, the user will then be prompted in the terminal to enter the actual measurement of the object to create a pixel to measurement scaling factor to be used in the tracking.
5. After a reference measurement has been established, the user will then be prompted to select the object of interest to track with a rectangular box. 
6. Finally, once the coordinate system, reference measurement, and object has been defined press the spacebar and the object tracking by frame will be shown in a new window to which the user can stop at any time by pressing ‘q.’
7. Once the tracking has finished or been stopped by the user, a text file and graph of the object position, velocity, acceleration, as a function of time will be written in a text file named data_values.txt and be displayed in a new interactive matplotlib window that can be exported.
