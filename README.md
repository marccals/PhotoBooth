# PhotoBooth
Photo booth with Raspberry Pi with Pi camera.
To exit app press Ctrl+C.

To execute it the following folders must be created inside PhotoBooth folder:
 * captured: Contains original captured image
 * composed: Contains composed image

***Dependencies***

Image magick: sudo apt-get install imagemagick
Pyhton Image library: sudo apt-get install python-imaging
CUPS Print server: sudo apt-get install cups

***How to add printer?***

Follow instructions of https://www.howtogeek.com/169679/how-to-add-a-printer-to-your-raspberry-pi-or-other-linux-computer/ to install CUPS print server and add printer
Then edit ComposeAndPrintfile.sh and set printer name in $printerName variable

***Disable screen saver***

http://www.etcwiki.org/wiki/Disable_screensaver_and_screen_blanking_Raspberry_Pi