import subprocess
import yaml
import re
import socket
import datetime
import reporter
import aggregator

properties = yaml.load(file('graphite_reporting.yaml', 'r'))


def start():
    f = subprocess.Popen(['tail', '-F', properties['log.file']], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line = f.stdout.readline()
        reporting = properties['reporting']
        for report in reporting:
            #TODO compile the regular expressions
            matchObj = re.match(report['filterRegex'], line)
            if matchObj:
                # Hostname is included so one can aggregate multiple environments together via graphite.
                tag = socket.gethostname() + '.' + report['pattern'].format(matchObj.groups())
                dateString = report['date'].format(matchObj.groups())
                date = datetime.datetime.strptime(dateString, properties['log.file.date.format'])
                date = date - datetime.timedelta(seconds=date.second)
                epocTime = date.strftime('%s')
                if properties['log.debug.enabled']:
                    print str(date) + " " + epocTime
                    print matchObj.groups()
                data = aggregator.aggregate(report['uniqueName'], tag, epocTime)
                reporter.report(uniqueName=report['uniqueName'], data=data, type=properties['reporting.tool'])
        continue


def main():
    start()

if __name__ == "__main__":
    main()