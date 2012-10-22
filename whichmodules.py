#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  multiple_cards.py
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



import os, re
import subprocess

def list_modules(directory):
    files = os.listdir(directory)

    path_list =[]
    
    different=True
    
    filepath = None
    
    for fl in files:
        fullpath =  os.path.join(directory, fl)
	if os.path.islink(fullpath):
	    for device in device_nums:
		    if device == '00.0':
			continue
		    test = re.compile("(.*)"+device+"(.*)")
		    if re.match(test, os.path.realpath(fullpath)):
			path_list.append(os.path.realpath(fullpath))
    newlist = []
		    
    for device in device_nums:
	if device == '00.0':
	    continue
	firstcopy=False;
	test = re.compile("(.*)"+device+"(.*)")
	for l in path_list:
	    if re.match(test, l) and not firstcopy:
		firstcopy=True
		newlist.append(l)
    
    path_list = set(newlist)  #eliminated duplicates
    
    drm_n=1;
    sound_n=1;
    eth_n=1
    wlan_n=1
    			
    if "drm" in directory:
	for path in path_list:
	    pci_path = os.path.realpath(path)
	    os.chdir(pci_path)
	    if os.path.islink("./device/driver"):
		module = os.path.basename(os.readlink("device/driver"))
		print "Video card %d:" % drm_n, module
		print re.sub('description:( *)', '', subprocess.check_output('modinfo ' + module + ' | grep "description:" --color=never', shell=True).strip('\n'))
		print
		drm_n+=1;
    elif "sound" in directory:
	for path in path_list:
	    pci_path = os.path.realpath(path)
	    os.chdir(pci_path)
	    if os.path.islink("./device/driver"):
		module = os.path.basename(os.readlink("device/driver"))
		print "Sound card %d:" % sound_n, module
		print re.sub('description:( *)', '', subprocess.check_output('modinfo ' + module + ' | grep "description:" --color=never', shell=True).strip('\n'))
		print
		sound_n+=1;
    elif "net" in directory:
	for path in path_list:
	    pci_path = os.path.realpath(path)
	    os.chdir(pci_path)
	    if os.path.islink("./device/driver"):
		module = os.path.basename(os.readlink("device/driver"))
		if re.match("(.*)eth(.*)", path):
		    print "Ethernet card %d:" % eth_n, module
		    print re.sub('description:( *)', '', subprocess.check_output('modinfo ' + module + ' | grep "description:" --color=never', shell=True).strip('\n'))
		    print
		    eth_n+=1
		else:
		    print "Wireless card %d:" % wlan_n, module
		    print re.sub('description:( *)', '', subprocess.check_output('modinfo ' + module + ' | grep "description:" --color=never', shell=True).strip('\n'))
		    print
		    wlan_n+=1

if __name__ == '__main__':

    pci_data = subprocess.check_output(["lspci", "-n"]).split('\n')
    pci_data.remove('')
    
    lspci_info = subprocess.check_output("lspci").split('\n')
    lspci_info.remove('')
    
    device_nums = []

    for device in pci_data:
	important = device.split()[0]
	important_nums = important.split(':')
	device_nums.append(important_nums[1])
    
    list_modules("/sys/class/drm/")

    list_modules("/sys/class/sound/")

    list_modules("/sys/class/net/")
    
    
