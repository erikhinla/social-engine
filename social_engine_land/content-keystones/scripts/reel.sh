#!/bin/sh
# Build a silent vertical reel from rendered frames, each held for its seconds, with short fades.
# Usage: sh scripts/reel.sh out.mp4 frame1.png:3 frame2.png:2.5 frame3.png:2.5
set -e
out=$1; shift
inputs=""; filters=""; n=0
for spec in "$@"; do
  f=${spec%:*}; d=${spec##*:}
  inputs="$inputs -loop 1 -t $d -i $f"
  filters="$filters[$n:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p,fade=t=in:st=0:d=0.12[v$n];"
  n=$((n+1))
done
concat=""; i=0; while [ $i -lt $n ]; do concat="$concat[v$i]"; i=$((i+1)); done
ffmpeg -y -loglevel error $inputs -filter_complex "${filters}${concat}concat=n=$n:v=1:a=0[out]" -map "[out]" -c:v libx264 -preset slow -crf 18 -movflags +faststart -pix_fmt yuv420p "$out"
echo "wrote $out"
