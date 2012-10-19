#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  autodetect.py
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

#Automatically detects hardware on Linux

import os, sys, re
import subprocess

def findmodules():
    print "Detecting modules..."
    print
    
    kernel_version = subprocess.check_output(["uname","-r"]).strip('\n')
    modules_alias = "/lib/modules/" + kernel_version + "/modules.alias"
    if not os.path.exists(modules_alias):
        if os.geteuid() != 0:
            print "Can't write module table since you are not root"
            sys.exit(1)
        print "Module table doesn't exist: regenerating..."
        p = subprocess.Popen("depmod")
        p.wait()
    try:
        file = open(modules_alias, 'r')
    except IOError:
        print "Error: That's strange, the module table should exist"
        sys.exit(1)
    module_list = file.readlines()
    for i in range(len(module_list)):
        module_list[i] = module_list[i].strip('\n')
    file.close()
    
    pci_data = subprocess.check_output(["lspci", "-n"]).split('\n')
    pci_data.remove('')
    lspci_info = subprocess.check_output("lspci").split('\n')
    lspci_info.remove('')
    which_device = 0
    for device in pci_data:
        important = device.split()[2]
        important_nums = important.split(':')
        regexp = "(.*)" + important_nums[0] + "(.*)" + important_nums[1] + "(.*)"
        lookfor = re.compile(regexp)
        for line in module_list:
            if re.match("(.*)pci(.*)", line.lower()):
                if re.match(lookfor, line.lower()):
                    the_device = lspci_info[which_device]
                    the_device = re.sub("^([0-9:\.]*) ", '', the_device)
                    the_device = re.findall("([A-Z]{1}.*:)", the_device)
                    print the_device[0], line.split(' ')[-1]
        which_device+=1


if __name__ == '__main__':
    
    #First make sure we are in the right environment
    if not sys.platform.lower().startswith("linux"):
        print "This script was developed for Linux"
        sys.exit(1)
    try:
        subprocess.call(["depmod", "--version"])
    except OSError:
        print "Missing Linux command"
        sys.exit(1)
    try:
        subprocess.call(["lspci", "--version"])
    except OSError:
        print "Missing Linux command"
        sys.exit(1)
    
    print
    
    #Now start looking for those modules
    findmodules()

