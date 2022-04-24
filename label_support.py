import sys, os, cv2

data_dir = ""
output_dir = ""

# ask for labels
print("Enter labels:\n")
label = " "
labels = []
while label != "":
    label = input("Enter new label, finish by entering empty ('') label: ")
    if label in labels:
        print("Duplicate labels! Not adding last label.")
    else:
        labels.append(label)
    print(labels)

if os.path.isdir(output_dir):
    action = input("An existing directory with the name {} was found.\nWould you like to append?(y/N)".format(output_dir))
    if action != "N":
        print("Correct the fault and run this script again.")
        exit(1)
    elif action == "y":
        pass # continue
    else: # unkown input
        print("Unknown input, exiting.")
        exit(1)
else:
    os.mkdir(output_dir)
    for l in labels:
        os.mkdir(os.path.join(output_dir, l))

for video_name in os.listdir(data_dir):
    video_file = os.path.join(data_dir, video_name)

    video = cv2.VideoCapture(video_file)

    if not video.isOpened():
        print("Could not open video {}. Skipping...".format(video_file))
        continue
       
    while video.isOpened():
        ret, frame = video.read()

        if ret:
            h, w, _ = frame.shape
            new_h = int(h / 2)
            new_w = int(w / 2)

            frame = cv2.resize(frame, (new_w,new_h))
            cv2.imshow(video_name, frame)

            if cv2.waitKey(15) != -1 and ord(' '):
                break
        else:
            break

    LABEL_PRINT_FORMAT = ["{}) {}\n",format(i+1,l) for i, l in enumerate(labels)].join()
    vid_label = input("What label should the video have?\n\n{}".format(LABEL_PRINT_FORMAT))
    vid_label = int(vid_label) -1

    target_name = os.path.join(output_dir, labels[vid_label], video_name)
    os.rename(video_file, target_name)
