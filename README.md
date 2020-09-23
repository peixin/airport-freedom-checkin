Scientific Internet Access

Automatically check in on the deyun platform everyday, just for knowledge freedom is more cost-effective.

- update user.config set user username password
  `mv user.config.template user.config`
  `vi user.config`

- You can use a scheduled task to run the script
  e.g.
  crontab
  `30 9 * * * /user-path/checkin.py >> /user-path/checkin.log 2>>&1`

- It is recommended to use cloud functions such as AWS Lamdba, Tencent Cloud SCF, Aliyun Function Compute etc.
