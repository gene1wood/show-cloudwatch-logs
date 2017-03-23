Tool to show AWS CloudWatch logs

# Usage

    usage: __init__.py [-h] [--profile PROFILE] [--region REGION]
                       [--showstreamname]
                       group [stream]
    
    Show CloudWatch logs
    
    positional arguments:
      group              CloudWatch Log Group name
      stream             CloudWatch Log Stream name
    
    optional arguments:
      -h, --help         show this help message and exit
      --profile PROFILE  AWS profile name
      --region REGION    AWS region
      --showstreamname   Just show the stream name
