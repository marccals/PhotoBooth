#!/bin/sh

printerName="VNC_Printer"

convert $1 -rotate 90 ./tmp/LeftPhoto.png & convert $1 -rotate -90 ./tmp/RightPhoto.png & wait

montage ./images/LeftTextPhoto.png ./tmp/LeftPhoto.png ./images/DashLine.png ./tmp/RightPhoto.png ./images/RightTextPhoto.png -tile 5x1 -geometry +0+0 $2

lp -d $printerName $2
