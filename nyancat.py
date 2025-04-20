import cv2
import time
import os
import sys
import subprocess
import multiprocessing

PWD = os.path.basename(__file__)

def rgb_to_ansi(r, g, b):
    return f"\033[48;2;{r};{g};{b}m "

def cleanup():
    print("\033[0m\033[?25h\033[2J\033[H")  # Reset colors, show cursor, clear screen
    sys.exit(0)

def signal_handler(sig, frame):
    cleanup()


def main():
    try:
        audio_process = subprocess.Popen(["ffplay", "-nodisp", "-autoexit", "-loop", "0", "nyancat.aac"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.5)
        if audio_process.poll() is not None:
            print("Audio process failed to start.")
            os._exit(1)

        # Hide cursor and clear screen
        print("\033[?25l\033[2J", end='')
        video = cv2.VideoCapture("nyancat.mp4")

        fps = video.get(cv2.CAP_PROP_FPS)
        secs_per_frame = 1 / fps

        while True:
            ret, frame = video.read()
            if not ret:
                # Cycle the video
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            # Convert frame to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            output = "\033[H"  # Move cursor to top-left
            for row in frame:
                for pixel in row:
                    r, g, b = pixel
                    output += rgb_to_ansi(r, g, b)
                output += "\033[0m\n"  # Reset color at end of line

            print(output, end='', flush=True)
            time.sleep(secs_per_frame - 0.018)
            
    except KeyboardInterrupt:
        cleanup()
        video.release()
        audio_process.kill()

if __name__ == "__main__":
    main()