#!/bin/bash
export PATH=$SNAP_APP_PATH:$SNAP_APP_PATH/bin:$PATH

#!/bin/bash

YOUTUBE_URL="__YOUTUBEURL__"  # URL youtube
YOUTUBE_KEY="__USERKEY__"   # User Key

ffmpeg -thread_queue_size 1024 -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f v4l2 -s 1280x720 -r 10 -i /dev/video0 -vcodec libx264 -pix_fmt yuv420p -preset ultrafast -r 25 -g 300 -b:v 2500k -codec:a libmp3lame -ar 44100 -threads 6 -b:a 256K -bufsize 512k -f flv "$YOUTUBE_URL/$YOUTUBE_KEY" 
