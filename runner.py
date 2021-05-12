import subprocess

while True:
    p = subprocess.Popen(['python', '-m', 'battleground', 'wambusters', 'DABABY_LESSGOOO'], shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='battleground')

    lines = p.stdout.readlines()

    win = lines[len(lines) - 1].decode('ascii')
    upper = lines[21].decode('ascii')
    lower = lines[22].decode('ascii')
    time = lines[len(lines) - 3].decode('ascii')

    print(time, upper, lower, win)
