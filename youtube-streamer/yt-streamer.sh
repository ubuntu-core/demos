#!/bin/bash
export PATH=$SNAP_APP_PATH:$SNAP_APP_PATH/usr/bin:$PATH

cred_path=$SNAP_APP_DATA_PATH/credentials
[ ! -f $cred_path ] && exit 0
. $cred_path

ffmpeg -thread_queue_size 1024 -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f v4l2 -s 1280x720 -r 10 -i /dev/video0 -vcodec libx264 -pix_fmt yuv420p -preset ultrafast -r 25 -g 300 -b:v 2500k -codec:a libmp3lame -ar 44100 -threads 6 -b:a 256K -bufsize 512k -f flv "$YOUTUBE_URL/$YOUTUBE_KEY" 
