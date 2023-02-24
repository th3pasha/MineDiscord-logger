with open('latest.log', 'r') as f:
    for line in f:
        if '[Server thread/WARN]' in line:
            continue
        if 'logged in with entity id' in line:
            continue
        if 'Disconnecting' in line:
            continue
        if 'Disconnected' in line:
            continue
        if '[Not Secure]' in line:
            continue
        if 'Timed out' in line:
            continue
        if 'com.mojang.authlib.GameProfile' in line:
            continue
        else:
            out_line = line.replace('[Server thread/INFO]', '')
            with open('log.log', 'a') as out_file:
                out_file.write(out_line)
