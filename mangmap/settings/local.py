import getconf

config = getconf.ConfigGetter(
    "mangmap",
    ["/etc/telescoop/mangmap/settings.ini", "./local_settings.ini"],
)

BACKUP_ACCESS = config.getstr("backup.backup_access")  # S3 ACCESS
BACKUP_SECRET = config.getstr("backup.backup_secret")  # S3 SECRET KEY
BACKUP_BUCKET = config.getstr("backup.backup_bucket")  # S3 Bucket
BACKUP_REGION = config.getstr("backup.backup_region", "eu-west-3")
