from dataclasses import dataclass

@dataclass
class Mod:
    name: str
    mod_id: str

    def __hash__(self):
        return hash((self.mod_id))
    
    def __eq__(self, other: object) -> bool: 
        return self.__hash__() == other.__hash__()

    @property
    def steam_id(self) -> str:
        """
        Returns the steam id of the mod. If the mod is local, it returns the local id.
        """
        if self.mod_id.startswith("local:"):
            return ""
        return self.mod_id