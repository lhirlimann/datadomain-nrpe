#!/usr/bin/python
import os
import sys
import optparse
import subprocess

snmpwalk = '/usr/bin/snmpwalk'
snmpget = '/usr/bin/snmpget'
community = ''
datadomains_fans_oid = '1.3.6.1.4.1.19746.1.1.3.1.1.1.6'
datadomains_disk_oid = '1.3.6.1.4.1.19746.1.6.3.1.1.14'
datadomains_battery_oid = '1.3.6.1.4.1.19746.1.2.3.1.1.3'


def check_snmp_walk(host, oid, description, compare_value, compare_type):
    counter = 0
    for r in subprocess.Popen(['%s -v2c -c %s -Oveqns %s %s' % (snmpwalk, community, host, oid)],stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].split():
        if compare_type == 'eq':
            if int(r) != compare_value:
                print "CRITICAL: Datadomain %s %i Failure. Return Value: %s" % (description, counter, r)
                sys.exit(2)
        if compare_type == 'gt':
            if int(r) <= compare_value:
                print "CRITICAL: Datadomain %s %i Failure. Return Value: %s" % (description, counter, r)
                sys.exit(2)
        if compare_type == 'lt':
            if int(r) >= compare_value:
                print "CRITICAL: Datadomain %s %i Failure. Return Value: %s" % (description, counter, r)
                sys.exit(2)
        counter += 1


def main(prog_args=None):
    
    if prog_args is None:
        prog_args = sys.argv
        
    parser = optparse.OptionParser()
    parser.usage = "Nagios check script to check various aspects of the datadomain"
    parser.add_option("-H", "--host", dest="host",
                      help="Type of check to run. [queue_count|queue_size]")
    opt, args = parser.parse_args(sys.argv[1:])
    if opt.host is None:
       print "Host is required"
       parser.print_help()
       sys.exit(2)
    else:
        check_snmp_walk(opt.host, datadomains_fans_oid, 'Fans', 1, 'eq')
        check_snmp_walk(opt.host, datadomains_disk_oid,'Disks status', 1, 'eq')
        check_snmp_walk(opt.host, datadomains_battery_oid, 'Battery status', 0, 'eq')
        print "OK: Datadomain Monitoring OK"
        sys.exit(0)

if __name__ == "__main__":
    main()
