from pathlib import Path
import json
from typing import List, MutableMapping, Set
import xmltodict
from .locations import Arma3LauncherLocations
from .mod import Mod
from .preset import Preset
import datetime

UNUSED_TAG = "UnusedMods"

class Arma3Launcher:

    def __init__(self, path: str | Path) -> None:
        self.locations = Arma3LauncherLocations(path)
        if not self.locations.root.exists():
            raise NotADirectoryError(self.locations.root)
        self._mods: MutableMapping[str,Mod] = {}
        self._mods_names_index: MutableMapping[str,Mod] = {}
        self._presets: set[Preset]= set()
        self.__load()

    @property
    def mods(self) -> Set[Mod]:
        return set(self._mods.values())
    
    
    @property
    def presets(self) -> Set[Preset]:
        return self._presets

    def __load(self):
        self.__load_mods(self.locations.steam)
        self.__load_presets(self.locations.presets)


    def __load_mods(self, path: Path):
        data = json.loads(path.read_text())
        self.localids = 0
        for row in data["Extensions"]:
            if "DisplayName" not in row or row["DisplayName"] == "":
                raise KeyError("Missing DisplayName in mods data")
            if "Id" not in row or row["Id"] == "":
                self.__add_local_mod(row["DisplayName"])
            else:
                self.__add_mod(Mod(name=row["DisplayName"], mod_id=row["Id"]))
        

    def __load_presets(self, path: Path):
        """
        Reads all preset files in the given path, parses them and adds them to the presets set.

        :param path: The path to the folder containing the preset files
        :type path: Path
        :return: None
        :rtype: None
        """
        presets = [(file.stem, xmltodict.parse(file.read_text(encoding= 'utf-8'))) for file in path.iterdir() if file.is_file()]
        try:
            for name, preset in presets:
                mods: Set[Mod] = set()
                mod = None
                if "addons-presets" in preset and "published-ids" in preset["addons-presets"] and preset["addons-presets"]["published-ids"]:
                    for id in preset["addons-presets"]["published-ids"]['id']:
                        
                        mod = self.__get_mod(id)
                        if mod is None:
                            mod=self.__add_local_mod(self.__local_mod_id_path_to_name(id))
                            mods.add(mod)
                        else:
                            mods.add(mod)
                self._presets.add(Preset(name, preset["addons-presets"]["last-update"], list(mods)))
        except KeyError:
            self._presets = set()
        unused_preset = {preset for preset in self._presets if preset.name == UNUSED_TAG}
        if unused_preset:
            self._presets.remove(unused_preset.pop())
        
    def __local_mod_id_path_to_name(self, id: str) -> str:
        id = id.replace("local:", "")
        if id.endswith("\\"):
            id = id[:-1]
        id.split("\\")[-1]
        id.replace("@", "")
        return id

    # Need to use both id and name to get the mod, because the name is not unique and the id is not unique either.
    def __get_mod(self, id: str) -> Mod | None:
        if id in self._mods:
            return self._mods[id]
        if id in self._mods_names_index:
            return self._mods_names_index[id]
        return None
        
    def __add_local_mod(self, name: str) -> Mod:
        if name in self._mods_names_index:
            return self._mods_names_index[name]
        self.localids += 1
        mod = Mod(name=name, mod_id="local:" + str(self.localids))
        self.__add_mod(mod)
        return mod
    
    def __add_mod(self, mod: Mod) -> None:
        if mod in self._mods:
            return 
        self._mods[mod.mod_id] = mod
        self._mods_names_index[mod.name] = mod


    def get_unused_mods(self) -> List[Mod]:
        unused_mods = set(self.mods)
        for preset in self.presets:
            for mod in preset.mods:
                if mod and mod in unused_mods:
                    unused_mods.remove(mod)
        return list(unused_mods)

    def make_unused_preset(self):
        preset_xml = Preset(UNUSED_TAG, datetime.datetime.now().isoformat(), self.get_unused_mods()).to_xml_string()
        with open(self.locations.presets / (UNUSED_TAG+'.preset2'), 'w',encoding= 'utf-8') as file:
            file.write(preset_xml)
        