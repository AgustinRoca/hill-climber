import time

from communication.client.client import MountainClient
from competition.hiker import *
from competition.team import Team

def main():
    
    
    # client = MountainClient('10.42.0.1', 8888)
    client = MountainClient('172.16.0.219', 8888)
    # client = MountainClient('localhost', 8080)
    teams = {}
    for i in range(20):
        hikers = []
        hikers.append(Hiker('Agus1', local_max_with_reset))
        hikers.append(Hiker('Agus2', local_max_with_reset))
        hikers.append(Hiker('Agus3', towards_random_point))
        hikers.append(Hiker('Agus4', random_circles))
        teams[f'LINAR{i}'] = Team(f'LINAR{i}', hikers)

        if not client.add_team(f'LINAR{i}', [hiker for hiker in teams[f'LINAR{i}'].members]):
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
            for hiker_name in data[team_name]:
                
                hiker = teams[team_name].get_member(hiker_name)
                hiker_data = data[team_name][hiker.name]
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
                if not next_iteration[hiker.name]['direction'] or not next_iteration[hiker.name]['speed']:
                    print(hiker.name)
                    print(hiker.prev_z, hiker.random_point)
                    print(next_iteration[hiker.name]['direction'], next_iteration[hiker.name]['speed'])
                    print(hiker_data)
            a = client.next_iteration(team_name, next_iteration)
        time.sleep(0.01)
    print('Competition over.')
    print('Final data:')
    print(client.get_data())
        

if __name__ == '__main__':
    main()
