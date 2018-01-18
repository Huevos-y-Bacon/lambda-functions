# AWS Lambda Function to delete EBS snapshots older than a specified number of days. 
#  FILTERS BASED ON SNAPSHOT DESCRIPTION. This is the only value that can be used to 
#  identify snapshots created via scheduled Storage Gateway volume snapshots

import boto3 
import collections 
import datetime

DRYRUN = "yes"
retention = 14

snapshot_descriptions = [
  'SGW*napshot',
  'Daily*',
  '*snapshot schedule',
  '*_temp',
  ] # multiple wildcards work, e.g. '*CreateIm*ami*7e2'

# GET THE CURRENT REGION
session = boto3.session.Session()
region = session.region_name

# DEFINE CONNECTION
ec2 = boto3.client('ec2',region)
owner_id = boto3.client('sts').get_caller_identity().get('Account')

# DEFINE FILTERS
filters = [
  {'Name': 'owner-id', 'Values': [owner_id]},
  {'Name': 'description', 'Values': snapshot_descriptions}
  ]

def lambda_handler(event, context): 
  mysnapshots = ec2.describe_snapshots(Filters=filters)
  now = datetime.datetime.today().strftime('%Y%m%d')
  current = int(now)
  snapcounter = 0
  for snapshot in mysnapshots['Snapshots']:
    # REMOVE TIME INFO FROM SNAPSHOT IN ORDER FOR COMPARISON TO WORK BELOW
    x = snapshot['StartTime'].strftime('%Y%m%d')
    snaptime = int(x)
    z = current - snaptime
    if z > retention:
      snapcounter = snapcounter + 1
      if DRYRUN != "yes":
        print "Snapshot %s (%s) is older than %s days (date: %s). Deleting." % (snapshot['SnapshotId'],snapshot['Description'],retention,snapshot['StartTime'])
        ec2.delete_snapshot(SnapshotId= snapshot['SnapshotId'])
      else:
        print "[DRYRUN] Snapshot %s (%s) is older than %s days (date: %s). Deleting." % (snapshot['SnapshotId'],snapshot['Description'],retention,snapshot['StartTime'])
  if snapcounter == 0:
    print "No snapshots to delete"
  else:
    print "Number of snapshots deleted: " + str(snapcounter)
