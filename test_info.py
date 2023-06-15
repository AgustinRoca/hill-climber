from communication.client.client import MountainClient

# client = MountainClient('10.42.0.1', 8888)
client = MountainClient('localhost', 8080)
info = client.get_mountain_info()
current_mountain = info['current_mountain']
current_mountain = current_mountain.split('.')[-1].split("'")[0]
current_time = info['time']
next_mountain = info['next_mountain']
next_mountain = next_mountain.split('.')[-1].split("'")[0]
print(f'Current mountain: {current_mountain}')
print(f'Current time: {current_time}')
print(f'Next mountain: {next_mountain}')