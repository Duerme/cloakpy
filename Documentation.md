***Duerme 03-07-2023*

## Simple spoofer

Below is a simple python program that takes the subprocess library and manually changes the mac address using system commands. We will be using the subprocess library to help us change the MAC address, in addition to adding fancy functionalities.

```python
#!/usr/bin/env python

import subprocess

subprocess.run("ifconfig eth0 down", shell=True) # brings down the interface to allow modification
subprocess.run("ifconfig eth0 hw ether 00:00:00:00:00:00", shell=True) # changes the AMC to 00...
subprocess.run("ifconfig eth0 up", shell=True) # brings interface back up 
  
```

## Taking user input

Below we are invoking the `input` method, which prompts the user to provide values that are then stored in a given variable.

```python
#!/usr/bin/env python

import subprocess

interface = input("interface > ") # User will prompted to provide interface
new_mac = input("desired MAC > ") # User will prompted to provide new MAC

subprocess.run(f"ifconfig {interface} down", shell=True) # brings down the interface to allow modification
subprocess.run(f"ifconfig {interface} hw ether {new_mac}", shell=True) # changes the AMC to 00...
subprocess.run(f"ifconfig {interface} up", shell=True) # brings interface back up 
  
```

### What is wrong with this code?

In the above example we are providing arguments to the subprocess module directly as a string. This method is not safe because it allows a user to abuse the command being run. If a user inputs the following  when prompted: `;ls;` the following command will be ran in the terminal, `ifconfig;ls;mac_input`. The semi colon is interperted as the end of a command, and anything written after is ran as it's own command. This will allow a user to inject their own commands. 

### How can we fix this?

Instead of using a string argument for the subprocess call, we can use an array. When providing python an array using subprocess, the first value is seen as the main command and the preceding values are just arguments. 

Here is the updated version:
```python
#!/usr/bin/env python

import subprocess

interface = input("interface > ")
new_mac = input("desired MAC > ")

subprocess.run(["ifconfig", interface, "down"], shell=True) # brings down the interface to allow modification
subprocess.run(["ifconfig", interface, "hw ether", new_mac], shell=True) # changes the AMC to 00...
subprocess.run(["ifconfig", interface, "up"], shell=True) # brings interface back up 
```

### How to provide arguments directly from command line

While our code is functional and takes in user input, it can be time consuming to run the program multiple times to change the MAC address. A solution to this problem is implementing the ability to pass arguments directly from the terminal. For example: `python3 mac_changer.py -i "eth0" -m "00:00:00:00:00:00"` would take the value after the `-i` switch, and pass it as an argument for interface while the value after the `-m` switch would specify your desired MAC address. 

In this block I will impliment the optparse library to enable command-line arguments:
```python
#!/usr/bin/env python

import subprocess
import optparse

parser = optparse.OptionParser()

parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address") # adds a switch with 2 possible variations: -i and --interface
parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")

(options, arguments) = parser.parse_args() # options variable will contain the user provided value. arguments variable will contain the switches.

interface = options.interface
new_mac = options.new_mac

print(f"[+] Changing {interface} MAC address to {new_mac}")

subprocess.run(["ifconfig", interface, "down"]) # brings down the interface to allow modification
subprocess.run(["ifconfig", interface, "hw", "ether", new_mac]) # changes the AMC to 00...
subprocess.run(["ifconfig", interface, "up"]) # brings interface back up
```

### Creating a function to promote code efficiency

A function in python is a block of code that can be ran once called. Depending on the format of your function, a user can add parameters that will be passed in as values in the code block. This will save us time in the future in case we are wanting to perfrom an action such as changing a MAC address. Instead of rewriting the code, we will have a funtion we can call on to perform the MAC address changes. In the following example we are creating a function called `change_mac` that will take two values: `interface & mac_address` and pass them into the code block. We then call the function at the end of our code and provide both values:

```python
#!/usr/bin/env python

import subprocess
import optparse

def change_mac(interface, mac_address):

    print(f"[+] Changing {interface} MAC address to {mac_address}")
    subprocess.run(["ifconfig", interface, "down"]) # brings down the interface to allow modification
    subprocess.run(["ifconfig", interface, "hw", "ether", mac_address]) # changes the AMC to 00...
    subprocess.run(["ifconfig", interface, "up"]) # brings interface back up 

parser = optparse.OptionParser()

parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address") # adds a switch with 2 possible variations: -i and --interface
parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")

(options, arguments) = parser.parse_args() # options variable will contain the user provided value. arguments variable will contain the switches.

change_mac(options.interface, options.new_mac)
```

### Now we will apply the same methodology to the argument parser

```python
#!/usr/bin/env python

import subprocess
import optparse

def get_arguments():

    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address") # Creates an Option object/Class and adds a switch with 2 possible variations: -i and --interface
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    return parser.parse_args() # returns the user provided arguments
    
def change_mac(interface, mac_address):

    print(f"[+] Changing {interface} MAC address to {mac_address}")
    subprocess.run(["ifconfig", interface, "down"]) # brings down the interface to allow modification
    subprocess.run(["ifconfig", interface, "hw", "ether", mac_address]) # changes the AMC to 00...
    subprocess.run(["ifconfig", interface, "up"]) # brings interface back up 

(options, arguments) = get_arguments() # options variable will contain the user provided value. arguments variable will contain the switches.
change_mac(options.interface, options.new_mac)
```

### Implementing conditional statements

We want to make sure that the user is providing arguments when running our code, so we will use conditional statements that will return an error if the user does not provide a required argument. In the following snippet we are implementing the conditional statements:

```python
#!/usr/bin/env python

import subprocess
import optparse

def get_arguments():

    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address") # Creates an Option object/Class and adds a switch with 2 possible variations: -i and --interface
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) =  parser.parse_args() # Assigns values to options and arguments
    if not options.interface: # if no interface is provided, print the following
        parser.error("[-] Please provide a network interface. Use --help or -h for more information.")
    elif not options.new_mac: # if no MAC is provided, print the following
        parser.error("[-] Please provide a new MAC address. Use --help or -h for more information.")
    return options

def change_mac(interface, mac_address):

    print(f"[+] Changing {interface} MAC address to {mac_address}")
    subprocess.run(["ifconfig", interface, "down"]) # brings down the interface to allow modification
    subprocess.run(["ifconfig", interface, "hw", "ether", mac_address]) # changes the AMC to 00...
    subprocess.run(["ifconfig", interface, "up"]) # brings interface back up 

options = get_arguments() # options variable will contain the user provided value.
change_mac(options.interface, options.new_mac)
```

### Using regex to extract the current MAC address

Python has a built-in library that can help us with extracting patterns in a string using regex. I am going to import the `re` library into the program. In the code below, you will see that I used the "search" method provided by `re` to find a desired pattern. The pattern: `\w\w:\w\w:\w\w:\w\w:\w\w:\w\w` will be used to extract the mac address from the results of `ifconfig`. To search for regex, you have to put the r before the quotations to let python know that you are providing regex filters and not escape patterns. 

```python
#!/usr/bin/env python3

import subprocess
import optparse
import re

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
# change_mac(options.interface, options.new_mac)

ifconfig_result = subprocess.check_output(["ifconfig", options.interface]).decode('utf-8') # returns the result of the ifconfig command
filtered_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result) # Pattern to match MAC addressing
print(filtered_result.group(0)) # Prints out first result
```

### Implementing a function and conditionals

Here I want to check if the MAC is what the user requested for it be, then print the appropriate statement if it's not. 

```python
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
current_mac = check_mac_addr(options.interface) # Pulls original MAC
print(f"[+] Current MAC = {current_mac}")

change_mac(options.interface, options.new_mac) # Changing MAC to desired address

if check_mac_addr(options.interface) != current_mac:
    print(f"[+] MAC address has been successfully changed to {options.new_mac}")
else:
    print(f"[-] MAC address has not been changed due to an error. Please make sure you are inputting the correct interface and a valid MAC address.")


```

## We're done!

The program is now capable changing the MAC address for a Linux system and checking to see if conditions are being met to give the user a more verbose output. The most important part of this lesson was leveraging the use of functions and libraries. The more simple and clean code is, the easier it will be to understand and troubleshoot.  
