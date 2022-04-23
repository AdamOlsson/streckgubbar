# Usage: python create_csv.py --datapath <path to video directory>
import sys, getopt, os, cv2

def search_csv(file, filename):
    return filename in file.read()
        

# read arg
try:
    opts, args = getopt.getopt(sys.argv[1:],"h:d:",["datapath="])
    if len(opts) == 0:
        raise ValueError
except:
    print("Usage:\npython create_csv.py --datapath <path to video directory>")
    sys.exit(2)

datapath = ""
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print("Usage\n python create_csv.py --datapath <path to video directory>")
        sys.exit()
    elif opt in ("-d", "--datapath"):
        datapath = arg

# evaluate if arg is valid path
if not os.path.isdir(datapath):
    raise ValueError("Could not find directory {}".format(datapath))

# ask for name of csv file
csv_filename = input("Please provide name for csv file:\n").split(".")[0]
cwd = os.getcwd()
csv_file = os.path.join(cwd, csv_filename + ".csv")
if os.path.isfile(csv_file):
    choice = input("Found file with the same filename. What would you like to do?\n1) Append to file.\n2) Overwrite existing file.\n3) Exit.\n\n")
    if choice == "1":
        print("Appending to existing file.")
        csv_filemode = "r+"
    elif choice == "2":
        print("Overwriting existing file.")
        csv_filemode = "w+"
    elif choice == "3":
        print("Exiting.")
        sys.exit(0)
    else:
        print("Invalid input, exiting...")
        sys.exit(2)
else:
    csv_filemode = "w+"

with open(csv_file, csv_filemode) as file:
    for video_name in os.listdir(datapath):
        
        video_file = os.path.join(datapath,video_name)

        if search_csv(file, video_name):
            # if video processed, skip
            print("Skipping {}".format(video_name))
            continue

        video = cv2.VideoCapture(video_file)
        fps = video.get(cv2.CAP_PROP_FPS)

        if not video.isOpened():
            print("Could not open video {}. Skipping...".format(os.path.join(datapath,video)))
            continue
       
        frame_idx = -1
        framenumbers = []
        ss = True  # indicate that next timestamp is start of new sequence
        print("New video.")
        while video.isOpened():
            ret, frame = video.read()
            frame_idx += 1
           
            if ret:
                h, w, _ = frame.shape
                new_h = int(h / 2)
                new_w = int(w / 2)

                frame = cv2.resize(frame, (new_w,new_h))
                cv2.imshow(video_name, frame)

                if cv2.waitKey(30) != -1 and ord(' '):
                    # create timestamp from frame_idx
                    timestamp_s = frame_idx/fps
                    timestamp_m = int(timestamp_s / 60)
                    timestamp_s = int(timestamp_s % 60)
                    if not ss:
                        timestamp_s += 1 # Always make sure end timestamp is 1s more than start
                    timestamp_str = "{:0>2}:{:0>2}".format(timestamp_m, timestamp_s)
                    print("{} noted!".format(timestamp_str))
                    framenumbers.append(timestamp_str)
                    ss = not ss
            else:
                break
       
        video.release()
        cv2.destroyAllWindows()

        # if uneven framenumbers, remove last
        if len(framenumbers) % 2 == 1:
            framenumbers = framenumbers[0:-1]

        file.write("{},{}\n".format(video_file, " ".join(framenumbers)))




