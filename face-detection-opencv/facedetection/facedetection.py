# -*- coding: utf-8 -*-
# Copyright (C) 2016 Canonical
#
# Authors:
#  Didier Roche
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import logging
import os
import cv2
import numpy
from time import time
import yaml

from datahandler import DataHandler
from settings import LAST_SCREENSHOT
from tools import Singleton, get_data_path, suppress

logger = logging.getLogger(__name__)


class FaceDetection(object):
    """Face detection handler class"""
    __metaclass__ = Singleton

    # Create the filter cascade
    faceCascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__), '..', 'logic.xml'))

    def __init__(self):
        """Save last screenshot at """
        self.faces_path = os.path.join(get_data_path(), LAST_FACES)
        self.screenshot_path = os.path.join(get_data_path(), LAST_SCREENSHOT)

    def detect_faces(self):
        logger.debug("Detect faces")
        # Read the image
        video_capture = cv2.VideoCapture(0)
        ret, image = video_capture.read()
        video_capture.release()

        # write the raw image to screenshot_path
        temp_file = "{}.new.png".format(self.screenshot_path)
        cv2.imwrite(temp_file, image)
        os.rename(temp_file, self.screenshot_path)

        # Detect faces in the image
        faces = self.faceCascade.detectMultiScale(
            image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        num_faces = len(faces)

        if num_faces > 0:
            logger.debug("{} faces detected".format(num_faces))
            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 36, 36), 5)

            temp_file = "{}.new.png".format(self.faces_path)
            cv2.imwrite(temp_file, image)
            os.rename(temp_file, self.faces_path)
            timestamp = time()

        # Introduce a bug on purpose in newer version

        # On older ubuntu core version, SNAP_VERSION is the sideloaded one, so we don't rely on that for now
        #if os.getenv("SNAP_VERSION", "0.1") != "0.1":
        #    num_faces = -10
        file_path = os.path.join(os.getenv("SNAP"), "meta", "snap.yaml")
        with suppress(IOError):
            with open(file_path, 'rt') as f:
                if yaml.load(f.read())["version"] != 0.1:
                    num_faces = -10

        DataHandler().add_one_facedetect_entry(int(time()), num_faces)
