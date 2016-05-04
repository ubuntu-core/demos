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

from servers import WebClientsCommands
from settings import LAST_SCREENSHOT
from tools import Singleton

logger = logging.getLogger(__name__)


class FaceDetection(object):
    """Face detection handler class"""
    __metaclass__ = Singleton

    # Create the filter cascade
    faceCascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__), '..', 'logic.xml'))

    def detect_faces(self):
        logger.debug("Detect faces")
        # Read the image
        video_capture = cv2.VideoCapture(0)
        ret, image = video_capture.read()
        video_capture.release()

        # Detect faces in the image
        faces = self.faceCascade.detectMultiScale(
            image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        if len(faces) > 0:
            logger.debug("{} faces detected".format(len(faces)))
            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 36, 36), 5)

            temp_file = "{}.new".format(LAST_SCREENSHOT)
            cv2.imwrite(temp_file, image)
            os.rename(temp_file, LAST_SCREENSHOT)
