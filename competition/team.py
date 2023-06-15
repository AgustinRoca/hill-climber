from competition.hiker import Hiker

class Team:
    def __init__(self, name, members):
        self.name = name
        self.members = {member.name: member for member in members}

    def get_member(self, name) -> Hiker:
        return self.members[name]

    