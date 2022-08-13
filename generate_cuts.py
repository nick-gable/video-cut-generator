"""generate_cuts: determine precise locations to cut videos based off of approximate positions fed in"""

import cv2
import files
import sys
import os


def get_fps(fname: str):
    """Returns frames per second of video at filename"""
    cap = cv2.VideoCapture(fname)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    return fps


def time_to_frame(time: str, fps: int):
    """Convert from time string (in HH:MM:SS, MM:SS, or SS format) to frame number based off of provided fps"""
    if time.count(":") > 2:
        print(f"Invalid time string: {time}")
        exit(1)
    times = time.split(":")
    times.reverse()
    # 60 ** i so that as we get further in time string, we are accounting for time factors of min/sec
    return sum([fps * (60 ** i) * int(times[i]) for i in range(len(times))])


def display_video(fname: str, loc: int, speed_mult: int=1):
    """Display a video at provided location, and check for keyboard events that indicate where user wants to place cut

    Pass fname in as an exact location (i.e. append data directory); loc is the *frame* to start video at

    Returns frame number where cut is selected by user"""
    cap = cv2.VideoCapture(fname)
    if not cap.isOpened():
        print("Error opening video file!")
        exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.set(cv2.CAP_PROP_POS_FRAMES, loc-1)
    frame_delay = int(1000/fps)  # needed to play video at right speed

    paused = False
    return_val = loc
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            if return_val < loc:
                # not up to predicted cut start location yet
                # this shouldn't run if skip works right
                return_val += 1
                continue
            cv2.imshow('Video', frame)

            key_val = cv2.waitKey(0 if paused else int(frame_delay/speed_mult)) & 0xFF
            if key_val == ord(' '):
                # toggle being paused
                paused = False if paused else True
            elif key_val == ord('f'):
                speed_mult *= 2
            elif key_val == ord('s'):
                speed_mult /= 2
            elif key_val == ord('m'):
                # user has picked a position
                break
            elif key_val == ord('r'):
                # user request a redo
                return_val = -1
                break
            elif key_val == ord('q'):
                # user requested out: abort!
                raise Exception("Aborting due to user request")
            elif key_val == ord('d'):  # advance the frame
                continue
            elif key_val == ord('k'):  # skip - bad times
                return_val = -2
                break

            return_val += 1
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

    if return_val == -1:
        # redo: call function again
        return display_video(fname, loc, speed_mult)
    elif return_val == -2:
        # skip this: times are bad
        return -1
    return return_val


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <data directory>")
        exit(1)
    directory = sys.argv[1]
    movies = files.get_movies(directory)
    clips = files.get_clips(directory)
    cuts = []
    try:
        for clip in clips:
            print(f'Cutting {clip["movie_id"]} for clip {clip["clip_id"]}')
            path = os.path.join(directory, movies[clip["movie_id"]])
            fps = get_fps(path)
            start_cut_frame = time_to_frame(clip["cut_start"], fps)
            end_cut_frame = time_to_frame(clip["cut_end"], fps)

            # try to subtract 2 seconds to give wiggle room in case cut isn't on
            start_cut_frame = start_cut_frame - 2*fps if start_cut_frame >= 2*fps else 0
            end_cut_frame = end_cut_frame - 2*fps if end_cut_frame >= 2*fps else 0

            actual_start = display_video(path, start_cut_frame)
            actual_start /= fps
            print("Start of cut marked at %.2fs" % actual_start)

            actual_end = display_video(path, end_cut_frame)
            actual_end /= fps
            print("End of cut marked at %.2fs" % actual_end)

            actual_start = actual_start if actual_start >= 0 else -1
            actual_end = actual_end if actual_end >= 0 else -1

            cuts.append({
                "clip_id": clip["clip_id"],
                "movie_id": clip["movie_id"],
                "start_sec": round(actual_start, 2),
                "end_sec": round(actual_end, 2)
            })

            print()
    except BaseException as err:
        print(f"Uncaught exception: {repr(err)}")
        print("An attempt will be made to write the completed cuts to file, but just in case...")
        print("Dumping existing cuts from memory: save these!")
        print(cuts)
    finally:
        files.write_cuts(directory, cuts)
        print("Cuts written to 'cuts.csv' in working directory, terminating generate_cuts")