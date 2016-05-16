# Here is a demo scripts helper

## Goal

We are demoing here 2 versions of face recognition via opencv (more info in the host ../README.md). 0.1 is the working one, 0.2 is broken on purpose (just build the package twice for your board and change 0.1 to 0.2 in snapcraft.yaml to trigger the broken behavior).

## Script

3 scripts helping for demoing are in that directory:
* `reinstall`: Used for initial installation/reset of the board. This can be useful if too many versions of the binary have been installed and you want to restart from a clean state, with snap allowed to access hardware.
* `update`: Update from 0.1 (working version) to 0.2 (broken on purpose).
* `rollback`: Rollback from 0.2 to 0.1, back in a working state.

## Warning

It's important to setup the board running the `reinstall` script. This is the only way for `rollback` to know to which version to rollback to (the last known good one) until snappy handles this.

## Files requirements

You need to set both `face-detection_0.1_<arch>.snap` and `face-detection_0.2_<arch>.snap` into the same directory you are going to run those 3 scripts.

If you create a `settings` file in the same directory than those scripts as per ../README.md, you will get it copied and used after running `reinstall`.
