#!/bin/sh
while :; do
	adb wait-for-device
	pm_stat=`adb shell pm path android | grep Error`
	[ "$pm_stat" = "" ] && break;
	echo "Android package manager not running, waiting 30s."
	sleep 30
done
