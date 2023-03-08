#!/usr/bin/env python3

import subprocess
import optparse
import re

def check_mac_addr(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8') # returns the result of the ifconfig command
    filtered_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if filtered_result:
        return filtered_result.group(0)
    else:
        print("[-] Could not read MAC address")
        return 0

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address") # Creates an Option object/Class and adds a switch with 2 possible variations: -i and --interface
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) =  parser.parse_args() # Assigns values to options and arguments
    if not options.interface:
        parser.error("[-] Please provide a network interface. Use --help or -h for more inforamtion.")
    elif not options.new_mac:
        parser.error("[-] Please provide a new MAC address. Use --help or -h for more information.")
    return options

def change_mac(interface, mac_address):
    print(f"[+] Changing {interface} MAC address to {mac_address}")
    subprocess.run(["ifconfig", interface, "down"]) # brings down the interface to allow modification
    subprocess.run(["ifconfig", interface, "hw", "ether", mac_address]) # changes the AMC to 00...
    subprocess.run(["ifconfig", interface, "up"]) # brings interface back up 

options = get_arguments() # options variable will contain the user provided value.
original_mac = check_mac_addr(options.interface) # Pulls original MAC
print(f"[+] Current MAC = {original_mac}")

change_mac(options.interface, options.new_mac) # Changing MAC to desired address

if check_mac_addr(options.interface) != original_mac: # Checks to see if MAC is different than the original
    print(f"[+] MAC address has been successfully changed to {options.new_mac}")
else:
    print(f"[-] MAC address has not been changed due to an error. Please make sure you are inputting the correct interface and a valid MAC address.")

