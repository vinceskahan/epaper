# epaper
This is based on the waveshare 2.13 v2 epaper demo example

```
## install python requirements
pip3 install -r requirements.txt

## run it manually
# hit ^C once to kill and run the clearscreen routines
# hit ^C twice to kill it immediately
python3 epaper.py

# or run it in the background
#   first you should symlink 'nohup.out' to /dev/null in your current
#   working directory so you don't write any output to nohup.out on disk

# then run the following command to background the program
nohup python3 epaper.py  &

# to run the clear screen routine manually
python3 epaper.py --clear

```

