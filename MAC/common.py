"""
Common definitions required for MAC library
"""

import copy
from dataclasses import dataclass
from os.path import exists as path_exists
from json import loads, JSONDecodeError
from .helpers import random_str

@dataclass
class Team:
    team_name: str
    members: list[str]

    def load():
        t = Team(
            f"Anonymous: <{random_str(6)}>",
            []
        )

        if path_exists("team.json"):
            with open("team.json", "r") as f:
                try:
                    v = loads(f.read())
                    t.team_name = v['team_name']
                    t.members = v['members']

                except JSONDecodeError:
                    pass
        
        return t
            
    def to_dict(self):
        return {
            "team_name": self.team_name,
            "members": copy.copy(self.members)
        }
