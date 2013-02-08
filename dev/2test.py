import subprocess

"""from http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html
"""
p = subprocess.Popen('./assaultcube.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout = []
while True:
    line = p.stdout.readline()
    stdout.append(line)
    print line,
    if line == '' and p.poll() != None:
        break
''.join(stdout)
