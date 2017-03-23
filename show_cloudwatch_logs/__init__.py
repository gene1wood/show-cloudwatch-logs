#!/usr/bin/python

import sys
import boto3
import argparse


class Printer():

    def __init__(self):
        self.x = True

    def display(self, line):
        if self.x:
            self.x = False
            print('\033[92m' + self.trim_guid(line.rstrip()) + '\033[0m')
        else:
            self.x = True
            print(self.trim_guid(line.rstrip()))

    def trim_guid(self, line):
        POSITION = 2
        TRIM_LENGTH = 2
        mf = line.split()
        if (len(mf) >= POSITION + 1 and
                len(mf[POSITION]) == 36 and
                mf[POSITION][8] + mf[POSITION][13] +
                mf[POSITION][18] + mf[POSITION][23] == '----'):
            mf[POSITION] = '**' + mf[POSITION][-TRIM_LENGTH:]
            return(' '.join(mf))
        else:
            return(line)


def get_args():
    parser = argparse.ArgumentParser(description='Show CloudWatch logs')
    parser.add_argument('group', type=str,
                        help='CloudWatch Log Group name')
    parser.add_argument('stream', nargs='?', type=str,
                        help='CloudWatch Log Stream name')
    parser.add_argument('--profile',
                        help='AWS profile name')
    parser.add_argument('--region',
                        help='AWS region')
    parser.add_argument('--showstreamname', action='store_true',
                        help='Just show the stream name')
    return parser.parse_args()


def print_stream(log_group_name, log_stream_name, printer, client):
    # Have to make our own paginator for get_log_events
    # https://github.com/boto/botocore/commit/2bcad3fefc99bfa600b3aa9e40f21cf89bc88f4b
    params = {'logGroupName': log_group_name,
              'logStreamName': log_stream_name,
              'startFromHead': True,
              'startTime': 0}
    last_token = None
    while last_token is None or last_token != params['nextToken']:
        last_token = params[
            'nextToken'] if 'nextToken' in params else None
        response = client.get_log_events(**params)
        params['nextToken'] = response['nextForwardToken']
        for event in response['events']:
            printer.display(event['message'])

            #         log_event_paginator = client.get_paginator('get_log_events')
            #         for event_page in log_event_paginator.paginate(logGroupName=log_group_name,
            #                                                        logStreamName=log_stream_name):


def main():
    args = get_args()
    s = boto3.Session(profile_name=args.profile, region_name=args.region)
    client = s.client('logs')
    log_group_name = args.group

    printer = Printer()
    log_stream_paginator = client.get_paginator('describe_log_streams')

    if args.stream is not None:
        stream_name_list = [args.stream]
    else:
        stream_list = []
        map(stream_list.extend, [x['logStreams'] for x in log_stream_paginator.paginate(logGroupName=log_group_name)])
        stream_name_list = [x['logStreamName'] for x in stream_list]

    for log_stream_name in stream_name_list:
        if args.showstreamname:
            print(log_stream_name)
        else:
            print_stream(log_group_name,
                         log_stream_name,
                         printer,
                         client)


if __name__ == "__main__":
    main()
