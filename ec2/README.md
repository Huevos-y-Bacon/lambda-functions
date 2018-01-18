# EC2 and related

## lambda_timebasedebssnapshotcleanup.py

Instead of using "deleteOn" or other tag-based methods of identifying and deleting snapshots, I needed a function that can calculate the age and delete based on that. I do use a filter based on Snapshot Description, since this seems to be the only way I can identify snapshots created by AWS Storage Gateway scheduled snapshots.

Set dryrun to "yes" and you might see logs like this:

```
START RequestId: cd94e627-fc75-11e7-bc40-a9331d290a54 Version: $LATEST
[DRYRUN] Snapshot snap-0df4e90dc6d8927fe (Daily snapshot) is older than 1 days (date: 2018-01-16 11:00:59+00:00). Deleting.
[DRYRUN] Snapshot snap-09f44b1ba117b01ec (Daily Snapshot) is older than 1 days (date: 2018-01-16 08:00:16+00:00). Deleting.
...
[DRYRUN] Snapshot snap-042bef3f06ee91469 (Daily Snapshot) is older than 1 days (date: 2018-01-05 08:00:27+00:00). Deleting.
Number of snapshots deleted: 24
END RequestId: cd94e627-fc75-11e7-bc40-a9331d290a54
REPORT RequestId: cd94e627-fc75-11e7-bc40-a9331d290a54	Duration: 413.03 ms	Billed Duration: 500 ms Memory Size: 128 MB	Max Memory Used: 45 MB	
```

A real run should look like this:

```
START RequestId: cd94e627-fc75-11e7-bc40-a9331d290a54 Version: $LATEST
Snapshot snap-06543b4a536e8dc21 (Daily Snapshot) is older than 1 days (date: 2018-01-14 08:00:09+00:00). Deleting.
Snapshot snap-0c43c87e61b3cc4b8 (Daily snapshot) is older than 1 days (date: 2018-01-13 11:01:28+00:00). Deleting.
...
Snapshot snap-042bef3f06ee91469 (Daily Snapshot) is older than 1 days (date: 2018-01-05 08:00:27+00:00). Deleting.
Number of snapshots deleted: 24
END RequestId: cd94e627-fc75-11e7-bc40-a9331d290a54
REPORT RequestId: cd94e627-fc75-11e7-bc40-a9331d290a54	Duration: 27413.03 ms	Billed Duration: 27500 ms Memory Size: 128 MB	Max Memory Used: 45 MB	
```

## Lambda test event

Create a test event in Lambda to make sure it works. The account Id is your own. The rule Arn can be copied from CloudWatch after the CloudFormation stack has been created.

```
{
  "account": "123456789012",
  "region": "eu-west-1",
  "detail": {},
  "detail-type": "Scheduled Event",
  "source": "aws.events",
  "time": "1970-01-01T00:00:00Z",
  "id": "cdc73f9d-aea9-11e3-9d5a-835b769c0d9c",
  "resources": [
    "arn:aws:events:eu-west-1:123456789012:rule/LambdaTest-LambdaTimeBasedEBSSnapshotsCleanup-J8FBPRDXJJYG"
  ]
}
```
