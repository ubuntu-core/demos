# Youtube streamer example demo

This demo illustrates how to reuse simple pieces from the Ubuntu distribution to build with minimal glue an Youtube live stream publishing.

## Hardware requirement:

You need a webcam attached to your snappy device to try this demo out.

## Install and use it:

### Install from the store:
```sh
sudo snappy install youtube-streamer-demo
```

### Using it:

The service will only starts once some youtube account will be configure. To do so, add something similar to this:

```sh
cat > /tmp/creds << EOF
config:
  youtube-streamer-demo:
    YOUTUBE_URL: "<rtmp://YOUTUBE_SERVER_URL>"
    YOUTUBE_KEY: "<YOUR_YOUTUBE_STREAM_KEY>"
EOF
```

Then, load this new config and remove the temporary file:
```sh
sudo snappy config youtube-streamer-demo /tmp/creds
rm /tmp/creds
```

The service should automatically start streaming to youtube. Please note that there is generally a 30s delay.

