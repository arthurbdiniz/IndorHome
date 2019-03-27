
#! /usr/bin/env python

import nmap
import time
import socket
import json
import sys
import os
import requests
import itertools
import ConfigParser
from collections import OrderedDict
from ConfigParser import RawConfigParser
from pymongo import MongoClient
import datetime
import time

# Scan you local network for all hosts
def scan():

  hosts= str(get_lan_ip()) + "/24"
  nmap_args = "-sn" #simple host discovery without portscan

  scanner = nmap.PortScanner()
  scanner.scan(hosts=hosts, arguments=nmap_args)

  hostList = []

  for ip in scanner.all_hosts():

    host = {"ip" : ip}

    if "hostname" in scanner[ip]:
      host["hostname"] = scanner[ip]["hostname"]

    if "mac" in scanner[ip]["addresses"]:
      host["mac"] = scanner[ip]["addresses"]["mac"].upper()

    hostList.append(host)

  return hostList


# Get your local network IP address. e.g. 192.168.178.X
def get_lan_ip():

  try:
    return ([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
  except socket.error as e:
    sys.stderr.write(str(e) + "\n") # probably offline / no internet connection
    sys.exit(e.errno)


# Read the config file
def parseConfigFile():

  scriptDir = os.path.dirname(os.path.realpath(__file__))
  configDir = os.path.join(scriptDir, "config.json")

  jsonFile = open(configDir)
  config = json.load(jsonFile)

  if len(config) < 1:
    sys.stderr.write("Oops, couldn't read the config file. Consult the readme.\n")
    sys.exit(0)

  try:
    # slackConfig = config["slack"]
    known_hosts = dict()

    for hostname, macs in config["hosts"].iteritems():
      known_hosts[hostname.title()] = [mac.upper() for mac in macs]

  except KeyError as e:
    sys.stderr.write("Please correct your config file. Missing section %s .\n" %str(e))
    sys.exit(0)

  if len(known_hosts) == 0:
    sys.stderr.write("Oops, you did not specify any known hosts. Please correct your config file.\n")
    sys.exit(0)

  return known_hosts


def postHost(recognizedHostsFormated):
    hosts = {'hosts': recognizedHostsFormated}
    result = posts.insert_one(hosts)
    print('One post: {0}'.format(result.inserted_id))

# Entry point
if __name__ == "__main__":

  KNOWN_HOSTS = parseConfigFile()

  # Init mongo config
  client = MongoClient()
  client = MongoClient('0.0.0.0', 27017)
  db = client.hosts_mac
  posts = db.posts

  # Initialize. Noone is here yet
  activeHosts = set()

  while True:

    scannedHosts = [host["mac"] for host in scan() if "mac" in host]
    # print scannedHosts

    recognizedHosts = set()
    recognizedHostsFormated = []

    for hostName, macs in KNOWN_HOSTS.iteritems():

      # print "Mac: ", macs

      for scannedHost in scannedHosts:

        # print scannedHost
        if scannedHost in macs:
          ts = time.time()
          timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
          post_data = {
              'name': hostName,
              'mac': macs,
              'time': timestamp
          }
          recognizedHosts.add(hostName)
          recognizedHostsFormated.append(post_data)

    # print recognizedHosts
    postHost(recognizedHostsFormated)

    # who joined the network?
    newHosts = recognizedHosts - activeHosts

    # who left the network?
    leftHosts = activeHosts - recognizedHosts

    print "----------------------------------"
    # print "left",leftHosts
    # print "joined", newHosts
    # print "activeHosts", activeHosts
    print "recognizedHosts", recognizedHosts

    # remember everyone for the next scan
    activeHosts = recognizedHosts

    # wait 60 seconds before trying again
    time.sleep(60)