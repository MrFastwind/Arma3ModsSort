from dataclasses import dataclass
from .mod import Mod

@dataclass
class Preset:
    name: str
    last_update: str
    mods: list[Mod]

    def __hash__(self):
        return hash((self.name))
    
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def to_xml_string(self) -> str:
        string ="""<?xml version="1.0" encoding="utf-8"?>
<addons-presets>
  <last-update>{time}</last-update>
  <published-ids>
""".format(time = self.last_update)

        for mod in self.mods:
            string += f"    <id>{mod.steam_id}</id>\n"

        string += """  </published-ids>
  <dlcs-appids />
</addons-presets>
        """
        return string