from socket import socket
import sys
import yaml

properties = yaml.load(file('graphite_reporting.yaml', 'r'))


def report(uniqueName, data, type):
    if type == 'graphite':
        sendToGraphite(uniqueName, data)
    else:
        raise Exception("{} is currently unsupported".format(type))


def sendToGraphite(uniqueName, data):
    lines = []
    sock = socket()
    try:
        sock.connect((properties['graphite.server'], properties['graphite.port']))
    except:
        print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" \
              % { 'server':properties['graphite.server'], 'port':properties['graphite.port']}
        sys.exit(1)

    for tag in data[uniqueName]:
        line = tag + ' ' + str(data[uniqueName][tag]['count']) + ' ' + str(data[uniqueName][tag]['time'])
        lines.append(line)
    message = '\n'.join(lines) + '\n'
    print "sending message\n"
    print '-' * 80
    print message
    print
    sock.sendall(message)