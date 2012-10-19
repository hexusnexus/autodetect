#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  whichmodules.py
#  
#  Copyright 2012 Jason Benjamin <hexusnexus@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import os
import subprocess

sound = os.path.basename(subprocess.check_output(['readlink', '/sys/class/sound/card0/device/driver/module']))
ethernet = os.path.basename(subprocess.check_output(['readlink', '/sys/class/net/eth0/device/driver/module']))
wireless = os.path.basename(subprocess.check_output(['readlink', '/sys/class/net/wlan0/device/driver/module']))

print "The module loaded for your sound card is:", sound 
print "The module loaded for your ethernet card is:", ethernet
print "The driver loaded for your wireless card is:", wireless
