# https://docs.opencv.org/4.x/index.html
import cv2
import os
import shutil

def extract_frames(frames_dir, interval_secs):

    print("Extracting frames to folder", frames_dir, "every", interval_secs, "seconds.")

    try:      
        # creating a folder named data
        if not os.path.exists(frames_dir):
            os.makedirs(frames_dir)
    
    # if not created then raise error
    except OSError:
        print ('Error: Creating directory of data')

    videos = []
    video_dir = "videos"
    for video_name in os.listdir(video_dir):

        print("\nReading:", video_name)
    
        # Read the video from specified path
        cam = cv2.VideoCapture(video_dir+"/"+video_name)

        # get the FPS of the video
        fps = round(cam.get(cv2.CAP_PROP_FPS))
        fpm = fps * 60
        frame_count = cam.get(cv2.CAP_PROP_FRAME_COUNT)
        video_length = round(frame_count/fps)

        print ("Video Length", video_length, "secs")
        print ("FPS:", fps)
        
        # frame
        currentframe = 1
        
        while(True):
            
            # reading from frame
            ret,frame = cam.read()
        
            if ret:
                # if video is still left continue creating images
                
                if (currentframe % (fps * interval_secs) == 0): 

                    currentsecond = int(currentframe / (fps * interval_secs))

                    # capture a frame every requested interval of seconds
                    name = './' + frames_dir + '/' + video_name + '_sec' + str(currentsecond) + '_frame' + str(currentframe) + '.jpg'
                    print ('Creating', name)
            
                    # writing the extracted images
                    cv2.imwrite(name, frame)
            
                # increasing counter so that it will
                # show how many frames are created
                currentframe += 1

            else:
                break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

def clean_up(frames_dir):
   shutil.rmtree(frames_dir)
   print("\nCleanup:", frames_dir, "directory deleted")


extract_frames("frames", 2)
clean_up("frames")