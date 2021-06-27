#!/home/justin/.pyenv/versions/3.8.1/bin/python3
'''
Created on Apr 18, 2020

@author: justin
'''

from pprint import pprint
import time
import os
import argparse
import re
import json
import getpass

from getmac import get_mac_address
from mac_vendor_lookup import MacLookup
import nmap
import psutil


def get_local_ipv4_interface_map():

    addrs = psutil.net_if_addrs()

    address_map = {}
    for interface, addresses in addrs.items():
        for address in addresses:
            # Value = 2 is for IPv4 address
            if address.family.value == 2:
                address_map[address.address] = interface

    return address_map


def get_hosts():

    scanner = nmap.PortScanner()
    print("starting scan")
    start = time.time()
    scanner.scan("172.16.80.0/23", "22", arguments="-n")
    print("completed scan", round(time.time() - start, 2))
    addresses = scanner.all_hosts()
    vendor_lookup = MacLookup()

    local_interface_map = get_local_ipv4_interface_map()

    hosts = []

    print("getting mac address of network cards")
    start = time.time()
    for address in addresses:
        mac = get_mac_address(ip=address)

        if not mac and address in local_interface_map:
            mac = get_mac_address(interface=local_interface_map[address])

        try:
            vendor = vendor_lookup.lookup(mac) if mac else None
        except KeyError:
            print("error processing mac for", address)
        hosts.append({"ip": address, "mac": mac, "vendor": vendor})
    print("mac address acquired", round(time.time() - start, 2))
    return hosts


def print_hosts():
    """
    prints the hosts on the network
    """

    hosts = get_hosts()
    pprint(hosts)


def update_hosts(args):
    """
    updates the /etc/hosts network file
    need to run the script in sudo mode

    we make the assumption that the name of the host 
    should be in the file only once

    args: (dict)
         a dict of arguments from args
    """

    if getpass.getuser() != "root" and not args["test"]:
        print("Run this with sudo rights or run in test mode")
        return

    hosts = get_hosts()
    with open(os.path.expanduser("/home/justin/.ssh/mac_map.json")) as handle:
        data = json.load(handle)

    # adding the host name to the list of hosts
    for host in hosts:
        if host["mac"] in data["machine_mac"]:
            host["machine"] = data["machine_mac"][host["mac"]]

    # build a hosts map
    machine_map = {host["machine"]: host for host in hosts if "machine" in host}
    with open("/etc/hosts") as handle:
        hosts_etc = handle.read().strip().split("\n")

    hostnames = set(data["hostname_machine_map"].keys())

    filtered_hosts = []
    # filters out lines where we had the hosts defined
    for line in hosts_etc:
        result = re.search("\s+(.+)$", line)
        hostname = result.groups()[0] if result else None
        if not result or hostname not in hostnames:
            filtered_hosts.append(line)

    # add the new host definitions
    new_etc_lines = []
    for hostname, machine in data["hostname_machine_map"].items():
        if machine in machine_map:
            new_etc_lines.append(f"{machine_map[machine]['ip']} {hostname}")
        else:
            print("This machine was not found on the network, not adding to hosts file", machine)

    etc_hosts_out = new_etc_lines + filtered_hosts

    out = "\n".join(etc_hosts_out)
    if args.get("test", False):
        print("contents to write to /etc/hosts")
        print(out)
        return

    print("writing the following content to /etc/hosts")
    print(out)
    with open("/etc/hosts", "w") as handle:
        handle.write(out)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Gets information of hosts in the network")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--write", action="store_true")

    args = parser.parse_args()

    args = vars(args)

    if args["write"]:
        update_hosts(args)
    else:
        pprint(get_hosts())
