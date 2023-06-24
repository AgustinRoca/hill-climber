from communication.client.client import MountainClient
import time

ip = '0.0.0.0'
port = 8888

while True:
    try:
        client = MountainClient(ip, port)

        m = client.get_mountain()
        print(chr(27) + "[2J")
        with open(f'leaderboards/{m}.txt') as f:
            lines = f.readlines()[:23]
                
            for idx,line in enumerate(lines):
                if idx >3:
                    lines[idx] = " ".join([f"{data:<10}" for data in line.split()]) + "\n"            
            
            while len(lines) < 23:
                lines.append('\n')

            s = ''.join(lines)
            print(s)
        time.sleep(5)
    except KeyboardInterrupt:
        exit(1)
    except:
        continue