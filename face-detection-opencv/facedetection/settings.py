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

import logger
import yaml
logger = logging.getLogger(__name__)

logger.debug("Opening settings file")
settings = {}
with open(os.path.join(get_data_path(), "settings"), 'r') as f:
    settings = yaml.load(f)["facedetection"]

WEBSERVER_PORT = int(settings.get("webserver-port", 8042))
SOCKET_PORT = WEBSERVER_PORT + 1

TIME_BETWEEN_SHOTS = int(settings.get("interval-shots", 10))
