#!/usr/bin/env python

import argparse
import csv
import glob
import math
import os
import sys
from collections import namedtuple
from operator import attrgetter
from Registry import Registry


class RegEntropy:
    """
    Main functionality of script. Parses the hive, finding data with specified entropy or higher.
    """

    def __init__(self, hive_file, min_entropy, min_bytes, as_csv):

        self.hive_file = hive_file
        self.min_entropy = min_entropy
        self.min_bytes = min_bytes
        self.as_csv = as_csv
        self.reg = Registry.Registry(self.hive_file)
        self.KeyEntropy = namedtuple('KeyEntropy', 'path value size entropy')
        self.hits = []

    def check_key(self, key):

        try:
            for value in key.values():
                if len(value.raw_data()) >= self.min_bytes:
                    entropy = calc_shannon(value.raw_data())
                    if entropy >= self.min_entropy:
                        self.hits.append(self.KeyEntropy(key.path(), value.name(), len(value.raw_data()), entropy))
        except Registry.RegistryParse.ParseException as parseEx:
            print "ParseException: {}".format(parseEx)
            print key.path()

        try:
            for subkey in key.subkeys():
                self.check_key(subkey)
        except Registry.RegistryParse.ParseException as parseEx:
            print "ParseException: {}".format(parseEx)
            print key.path()

    def analyse(self):

        print('[{}]'.format(self.hive_file))
        self.check_key(self.reg.root())

        if 1 > len(self.hits):
            print 'no data found with a high enough entropy'
        else:
            if self.as_csv:
                self.to_csv()
            else:
                self.to_text()

    def to_text(self):

        for key_ent in sorted(self.hits, key=attrgetter('entropy'), reverse=True):
            path = '\\'.join(key_ent.path.split('\\')[1:])
            print('{:.5f} {:<9} {}\\{}'.format(key_ent.entropy, key_ent.size, path, key_ent.value))

    def to_csv(self):

        csv_writer = csv.writer(sys.stdout, quotechar='"')

        csv_writer.writerow(['hivefile', 'entropy', 'size', 'key'])
        for key_ent in sorted(self.hits, key=attrgetter('entropy'), reverse=True):
            path = '\\'.join(key_ent.path.split('\\')[1:])
            csv_writer.writerow([self.hive_file, key_ent.entropy, key_ent.size, path+'\\'+key_ent.value])


def calc_shannon(data):
    """
    Calculates the Shannon entropy of data. The closer to 8, the higher the entropy.
    :param data: Calculate the Shannon entropy of this data
    :return: A float between 0 and 8
    """

    byte_array = map(ord, data)
    data_size = len(byte_array)

    # calculate the frequency of each byte value
    byte_count = [0 for b in xrange(256)]
    for b in byte_array:
        byte_count[b] += 1
    byte_freq = []
    for c in byte_count:
        byte_freq.append(float(c) / data_size)

    # Shannon entropy
    ent = 0.0
    for freq in byte_freq:
        if freq > 0:
            ent += freq * math.log(freq, 2)
    return ent * -1


if __name__ == '__main__':

    argp = argparse.ArgumentParser()
    argp.add_argument('target', nargs='+', help='file to analyse. supports globbing: folder{0}*'.format(os.sep))
    argp.add_argument('--min-ent', '-e', type=float, default=7.0,
                      help='show hits with at least this entropy (default=7.0)')
    argp.add_argument('--min-bytes', '-b', type=int, default=128,
                      help='ignore data less than this many bytes (default=128)')
    argp.add_argument('--csv', '-c', help='output in CSV format', action='store_true')
    args = argp.parse_args()

    targets = []
    for t in args.target:
        if os.path.isfile(t):
            targets.append(t)
        else:  # try and glob
            [targets.append(tmp) for tmp in glob.glob(t)]

    if len(targets) < 1:
        print('no valid files found. nothing to do.')
    else:
        for t in targets:
            analyser = RegEntropy(t, args.min_ent, args.min_bytes, args.csv)
            analyser.analyse()
