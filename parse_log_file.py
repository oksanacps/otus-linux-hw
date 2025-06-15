#!/usr/bin/env python3
import json
import os
from collections import Counter
import argparse

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
        methods.append(line.split()[5].strip('" '))
        long_duration.append((int((line.split()[-1])), line))

    data["top_ips"] = dict(Counter(ips).most_common(3))
    data["total_stat_by_method"] = dict(Counter(methods))
    long_duration.sort(reverse=True)
    long_duration_lines = long_duration[:3]
    for line_duration in long_duration_lines:
        line_duration_ls = line_duration[1].split()
        request_info = {
            'ip': line_duration_ls[0],
            'date': ' '.join(line_duration_ls[3:5]),
            'method': line_duration_ls[5].strip('" '),
            'url': line_duration_ls[6],
            'duration': line_duration_ls[-1]
        }
        top_list.append(request_info)

    data["top_longest"] = top_list
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('log_file_path', help='Path to the directory to analyze log file')
    args = parser.parse_args()

    if os.path.isdir(args.log_file_path):
        log_files = [args.log_file_path + i for i in os.listdir(args.log_file_path) if i.endswith('.log')]
        for log_file in log_files:
            data = analyze_logs(log_file)
            json_data = json.dumps(data, ensure_ascii=False, indent=2)
            print(json_data)
    else:
        print(f"Error: Path {args.log_file_path} does not exist or is not accessible")

if __name__ == "__main__":
    main()