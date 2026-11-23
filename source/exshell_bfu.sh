#!/bin/sh
# V380 experimental read-only ID and hardware probe.
# Camera-side writes: microSD only. No raw flash reads or writes.
PATH=/bin:/sbin:/usr/bin:/usr/sbin
umask 077
SD=""
for d in /mnt/sdcard /sdcard /media/mmcblk0p1 /mnt/mmc /mnt/sd; do
  if [ -d "$d" ] && [ -w "$d" ]; then SD="$d"; break; fi
done
[ -n "$SD" ] || exit 3
D="$SD/V380_ID_RESULT"
mkdir -p "$D" || exit 4
LOG="$D/00_RESULT.txt"
{
  echo 'V380_ID_PROBE_STARTED'
  date 2>/dev/null
  echo '--- Kernel / processor ---'
  uname -a 2>/dev/null
  cat /proc/cpuinfo 2>/dev/null
  echo '--- Config and identity ---'
  for f in /mnt/mtd/network_Info.ini /mnt/mtd/network_info.ini /mnt/mtd/mvconf/network_Info.ini /mnt/mtd/mvconf/version.ini /mnt/mtd/mvconf/patchmanage.conf /mnt/mtd/version.ini /mnt/mtd/hwname /mnt/mtd/hwprefix /mnt/mtd/mvconf/dev_info.ini; do
    if [ -f "$f" ]; then
      echo "FILE=$f"
      grep -iE '(^|[^a-z])(dev_id|device_id|hwname|hwprefix|hw_|version|soft_id|serial|ssid|mac)[^a-z]' "$f" 2>/dev/null | sed -n '1,100p'
      case "$f" in
        */patchmanage.conf|*/version.ini|*/hwname|*/hwprefix) head -c 8192 "$f" 2>/dev/null ;;
      esac
      echo
    fi
  done
  echo '--- Filesystem summary ---'
  ls -la /mnt/mtd /mnt/mtd/mvconf 2>/dev/null | sed -n '1,100p'
  echo '--- Flash partition names (NOT contents) ---'
  cat /proc/mtd 2>/dev/null
  echo 'V380_ID_PROBE_FINISHED'
} > "$LOG" 2>&1
sync
exit 0
