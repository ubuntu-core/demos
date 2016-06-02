# Face detection example demo

This demo illustrates how to reuse simple pieces from the Ubuntu distribution to detect and count the number of people stopping
by at a booth. It has as well a `demo-scripts/` directory which contains script to reinstall, update and rollback to show up
the rollback mecanism.

## Hardware requirement:

You need a webcam attached to your snappy device to try this demo out.

## Install and use it:

### Install from the store:
```sh
sudo snap install face-detection-demo --devmode
```

### Using it:

The service will start automatically and you can head over to http://localhost:8042 to get your camera starts counting persons through face detection.

You will see there a graph updating automatically every 10s with the new data and showing off the last photo where someone was detected.

### Settings:

Some settings are available for you to tweak. You need to create a `settings` file in `$SNAP_DATA` before the service exits. Note that
the reinstall scripts does this if you set the `settings` file next to it before executing.

The `settings` file itself is a yaml format configuration, which can contain:
```
facedetection:
  webserver-port: 8042
  interval-shots: 10
```

`webserver-port` enable changing the ports where the web server listen at. `interval-shots` is the interval between 2 shots in seconds.
