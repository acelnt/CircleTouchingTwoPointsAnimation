"""CircleThroughTwoPoints.py

Generates an animation consisting of two points and a circle. The centre of the circle moves from left to right and the
radius of then circle changes to allow the circle to touch the points. Additional information is also shown.
"""
import cv2
from CreateFrames import *

INITIAL_X = -6000
FINAL_X = 6000
STEP = 10

OUTPUT_FILENAME = "video.mp4"
FPS = 60

def main():
    # If frames or the video have been created, delete them
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)
    if os.path.exists(FRAMES_PATH):
        clear_frames_directory()

    create_frames(INITIAL_X, FINAL_X, STEP)
    print("frames created")
    join_frames(OUTPUT_FILENAME, FPS)
    print("video created")


def clear_frames_directory():
    """Remove all the files with the prefix 'frame' in the frames directory"""
    for file in os.listdir(FRAMES_PATH):
            if file[:5] == "frame":
                os.remove(FRAMES_PATH + "/" + file)


def join_frames(filename, fps):
    """Creates a video from the frames in ./frames and saves it with the filename 'filename', using fps, 'fps'"""
    
    video = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), fps,
                            FRAME_SIZE)

    frame_filenames = sorted(os.listdir(FRAMES_PATH),
                    key=lambda x: int(x[5:-4]))
    for frame_filename in frame_filenames:
        frame_image = cv2.imread(FRAMES_PATH + "/" + frame_filename)
        video.write(frame_image)

    video.release()


if __name__ == "__main__":
    main()
