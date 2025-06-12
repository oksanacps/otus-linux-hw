#!/usr/bin/env python3
import argparse
import os
import json
from collections import Counter
import re
from pprint import pprint
import sys

data = {
    "total_requests": 0,
    "total_stat_by_method": {},
    "top_ips": {},
    "top_longest": []   
}


def analyze_logs(log_file):
    ips = []
    methods = []
    long_duration = []
    top_list = []

    with open(log_file, 'r') as file:
        lines = file.readlines()
    for line in lines:
        data["total_requests"] += 1
        ips.append(line.split()[0])
        methods.append(line.split()[5])
        long_duration.append((int((line.split()[-1])), line))

    data["top_ips"] = dict(Counter(ips).most_common(3))
    data["total_stat_by_method"] = dict(Counter(methods))
    long_duration.sort(reverse=True)
    long_duration_lines = long_duration[:3]
    print(long_duration_lines)
    for line_duration in long_duration_lines:
        print(line_duration[1])
        top_list.append(line_duration[1][:2] + line_duration[1][3:5] + line_duration[1][7:8] + line_duration[1][-1])

    data["top_longest"] = top_list
    return data

def main():
    current_dir = os.getcwd()
    log_files = [f for f in os.listdir(current_dir) if f.endswith('.log')]
    for log_file in log_files:
        data = analyze_logs(log_file)
        # json_data = json.dumps(data, indent=2)
    pprint(data)

if __name__ == "__main__":
    main()