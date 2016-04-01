ffmpeg -framerate 3 -s 1920x1080 -i %d.png -c:v libx264 -preset ultrafast -tune stillimage  out.avi
