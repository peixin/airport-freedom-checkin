Scientific Internet Access

Automatically check in on the deyun platform everyday, just for knowledge freedom is more cost-effective.

- update user.config set user username password
  `cd _data && mv user.config.template user.config`
  `vi user.config`

- You can use a scheduled task to run the script
  e.g.
  crontab
  `30 9 * * * /user-path/run.py`

- It is recommended to use cloud functions such as AWS Lamdba, Tencent Cloud SCF, Aliyun Function Compute etc.
