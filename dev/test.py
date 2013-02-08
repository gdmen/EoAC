import time
import subprocess

def follow(thefile):
    thefile.seek(0,2)      # Go to the end of the file
    while True:
         line = thefile.readline()
         if not line:
             time.sleep(0.1)    # Sleep briefly
             continue
         yield line

acfile = open("logfile.txt", "w+")
logfile = open("logfile.txt", "r")

ac_client = subprocess.Popen(["/home/gm/AssaultCube/1.1.0.4/bin_unix/linux_client", "--home=/home/gm/.assaultcube_v1.1", "--init"],
                             stdin = subprocess.PIPE,
                             stdout = acfile,
                             universal_newlines = True,
                             stderr = subprocess.STDOUT)

ac_client.stdin.write("\n");
loglines = follow(logfile)
for line in loglines:
    print line

print "DONE"
"""
# Avoid having to re-interpret dot notation in the loop
ac_readline = ac_client.stdout.readline
logger.debug('(main): Start parsing loop.')
while True:
    line = ac_readline()
    if not line or ac_client.poll() != None:
        raise KeyboardInterrupt()
    ac_client.stdin.write('\n')
    ac_client.stdin.flush()
    parser.parseLine(line, screenshot_taken_in_queue)
"""
