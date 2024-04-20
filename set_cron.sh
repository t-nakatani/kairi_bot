#!/bin/sh

crontab /work/cron.txt
# Start the cron daemon
cron -f
