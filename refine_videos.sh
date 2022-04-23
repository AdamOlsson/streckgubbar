#!/bin/bash
# Use a file as input: ./refine_videos.sh --csv example_csv.csv --output newdataset

while getopts f:o: flag
do
    case "${flag}" in
        f) CSV_FILE=${OPTARG};;
        o) OUTPUT_DIR=${OPTARG};;
    esac
done

mkdir $OUTPUT_DIR

# Read csv file
OLDIFS=$IFS
IFS=','
[ ! -f $CSV_FILE ] && { echo "$CSV_FILE file not found"; exit 99; }
while read filename timestamps
do
    # Storing as array into myarray
    TEMPIFS=$IFS
    IFS=" " read -a ts <<< $timestamps
    IFS=$TEMPIFS
	
    for (( i=0; i<${#ts[@]}; i=i+2 ));
    do
        NEWFILENAME=$(md5sum<<<"$filename + $i")
        NEWFILENAME="${NEWFILENAME:0:32}.mp4" # Remove trailing char from md5sum str
        OUTPUTFILE="$OUTPUT_DIR/${NEWFILENAME}"

        if [[ ! -f "$OUTPUT_DIR/$NEWFILENAME" ]]; then
            (set -x; ffmpeg -hide_banner -loglevel warning -ss ${ts[$i]} -to ${ts[$i+1]} -i ${filename} -c copy ${OUTPUTFILE})
            if [ $? -eq 0 ]; then
               echo "DONE"
            else
               echo "FAIL"
               exit 1
            fi
        fi

    done
done < $CSV_FILE
IFS=$OLDIFS
