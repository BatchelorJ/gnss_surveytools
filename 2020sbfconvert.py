#!/usr/bin/env python

# SBF to RINEX 2.11 Hatanaka Compressed Gzipped Converter

__author__ = "Josh Batchelor, Surveyor-General Victoria"
__maintainer__ = "Josh Batchelor"
__email__ = "josh.batchelor@delwp.vic.gov.au"
__status__ = "Prototype"

import os
from math import sqrt
import pathlib
import fileinput
import sys
import glob
import getopt


def htchk(metric, imperial):
    return round(metric - (imperial * (1 / 3.28)), 4)


def bon2bam(ht_bon):
    # Convert Bottom of Notch Height to Bottom of Antenna Mount for Trimble Zephyr Geodetic 3 Antenna
    return round((sqrt(ht_bon ** 2 - 0.16891 ** 2) - 0.04434), 4)


def sbfconvdir(sbfdir, year):
    # get list of .sbf files in dir
    sbflist = []
    for (dirpath, dirnames, filenames) in os.walk(sbfdir):
        sbflist = (f for f in filenames if f.endswith('.sbf'))
        break
    # Run converter for all sbf files
    if sbflist == []:
        pass
    else:
        for num, fn in enumerate(sbflist):
            sbf2rinh(pathlib.Path(sbfdir + '/' + fn), year)
            # print('Converted File ' + str(num + 1) + ' of ' + str(len(list(sbflist))))
            # file, ext = os.path.splitext(fn)
            # hatanaka_gzip(pathlib.Path(sbfdir + '/' + file + '.' + year + 'D'))


def anthtcalc(ant_file):
    # Read and format file contents
    with open(ant_file) as f:
        ant_strings = f.readlines()
    ant_ht_info = []
    for line in ant_strings:
        ht_info = line.rstrip()
        ant_ht_info.append(ht_info.split(','))
    # Calculate Imperial to Metric Diff and Bottom of Antenna Mount Heights
    for num, ant_ht in enumerate(ant_ht_info):
        bon_ht = float(ant_ht[1])
        bon_imperial = float(ant_ht[2])
        imperial_chk = htchk(bon_ht, bon_imperial)
        bam_ht = bon2bam(bon_ht)
        ant_ht_info[num][1] = bon_ht
        ant_ht_info[num][2] = bon_imperial
        if len(ant_ht) >= 5:
            ant_ht_info[num][3] = imperial_chk
            ant_ht_info[num][4] = bam_ht
        else:
            ant_ht_info[num].append(imperial_chk)
            ant_ht_info[num].append(bam_ht)
    # Output newly calculated values to text file
    with open(ant_file, 'w') as f:
        for i in ant_ht_info:
            f.write(','.join([str(x) for x in i]) + '\n')


def sbf2rinh(fn, year):
    # Converts sbf file to RINEX 2.11
    file, ext = os.path.splitext(fn)
    os.system("sbf2rin -f {1} -o {0}.{2}O".format(file, file + ext, year))
    # Get Height from Antenna Height File
    with open(dirname + '\\ZephyrAntHt.txt') as f:
        for line in f.readlines():
            if line.startswith(os.path.split(file)[1]):
                ht_info = line.rstrip()
                ht_info = ht_info.split(',')
                ant_ht = ht_info[4]
    # Add Height to Rinex File
    add_rinex_ht(file + '.' + year + 'O', ant_ht)
    # Hatanaka-compress Rinex File
    os.system("rnx2crx {0}.{1}O".format(file, year))
    os.remove(file + '.' + year + 'O')


def add_rinex_ht(file, ant_ht):
    for line in fileinput.input(file, inplace=True):
        line = line.rstrip('\r\n')
        if line == '        0.0000        0.0000        0.0000                  ANTENNA: DELTA H/E/N':
            print(line[:8] + str(ant_ht).ljust(6, '0') + line[14:])
        else:
            print(line)


def hatanaka_gzip(fn):
    os.system("gzip {0}".format(fn))
    pass


if __name__ == "__main__":  # code to execute if called from command-line
    dir_path = os.path.abspath(os.path.realpath(__file__))
    dirname, fname = os.path.split(dir_path)
    YY = fname[2:4]
    anthtcalc(dirname + '\\ZephyrAntHt.txt')
    sbfconvdir(dirname, YY)
    pass
