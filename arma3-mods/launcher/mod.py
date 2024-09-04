from dataclasses import dataclass

@dataclass
class Mod:
    name: str
    steam_id: str

    def __hash__(self):
        return hash((self.steam_id))
    
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

