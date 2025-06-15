# otus-linux-hw

## Log File Analyzer

This script analyzes log files and provides statistics about HTTP requests.

### Features

The script analyzes log files and provides the following information:
- Total number of requests
- Statistics by HTTP method (GET, POST, etc.)
- Top 3 IP addresses by number of requests
- Top 3 longest requests with detailed information

### Usage

```bash
python parse_log_file.py <path_to_log_file_or_directory>
```

Note: When specifying a directory path, it must end with a forward slash (/). For example:
```bash
python parse_log_file.py /path/to/logs/
```

### Output Format

The script outputs JSON with the following structure:
```json
{
  "total_requests": <number>,
  "total_stat_by_method": {
    "<method>": <count>,
    ...
  },
  "top_ips": {
    "<ip>": <count>,
    ...
  },
  "top_longest": [
    {
      "ip": "<ip_address>",
      "date": "<request_date>",
      "method": "<http_method>",
      "url": "<requested_url>",
      "duration": "<request_duration>"
    },
    ...
  ]
}
```

### Requirements

- Python 3.x
- No additional dependencies required

### Input Format

The script expects log files in a standard format where each line contains:
- IP address
- Request method
- URL
- Duration
- Other standard log information

### Notes

- The script can process directories containing multiple .log files
- Results are printed to stdout in JSON format