import time

from communication.client.client import MountainClient
from competition.hiker import Hiker, local_max, random_walk, towards_random_point, random_circles
from competition.team import Team

def main():
    
    hikers = []
    hikers.append(Hiker('Bot1', local_max))
    hikers.append(Hiker('Bot2', random_walk))
    hikers.append(Hiker('Bot3', towards_random_point))
    hikers.append(Hiker('Bot4', random_circles))
    client = MountainClient('10.42.0.1', 8888)
    # client = MountainClient('localhost', 8080)
    for i in range(1):
        team = Team(f'Bolton Dynamics{i}', hikers)

    
        if not client.add_team(team.name, [hiker for hiker in team.members]):
            print('Team could not be registered. Registration already over?')
            exit(1)
    # client.finish_registration()

    while client.is_registering_teams():
        time.sleep(0.1)
    
    while not client.is_over():
        data = client.get_data()
        print(data)
        for team_name in data:
            next_iteration = {}
            if team_name == team.name:
                for hiker_name in data[team_name]:
                    
                    hiker = team.get_member(hiker_name)
                    hiker_data = data[team.name][hiker.name]
                    x = hiker_data['x']
                    y = hiker_data['y']
                    z = hiker_data['z']
                    dx = hiker_data['inclinacion_x']
                    dy = hiker_data['inclinacion_y']
                    summit = hiker_data['cima']

                    hiker.set_position(x, y, z, dx, dy, summit)
                    if not summit:
                        next_iteration[hiker.name] = {}
                        next_iteration[hiker.name]['direction'] = hiker.next_direction()
                        next_iteration[hiker.name]['speed'] = 50
                a = client.next_iteration(team_name, next_iteration)
        time.sleep(0.1)
    print('Competition over.')
    print('Final data:')
    print(client.get_data())
        

if __name__ == '__main__':
    main()
