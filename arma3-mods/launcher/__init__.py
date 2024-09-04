from pathlib import Path
import json
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
        self._mods = set()
        self._presets = set()
        self.__load()

    @property
    def mods(self) -> [Mod]:
        return self._mods
    
    
    @property
    def presets(self) -> [Preset]:
        return list(self._presets)

    def __load(self):
        self.__load_mods(self.locations.steam)
        self.__load_presets(self.locations.presets)


    def __load_mods(self, path: Path):
        data = json.loads(path.read_text())
        self._mods = {Mod(name=row["DisplayName"], steam_id=row["Id"]) for row in data["Extensions"]}

    def __load_presets(self, path: Path) -> None:
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
                mods = set()
                if "addons-presets" in preset and "published-ids" in preset["addons-presets"] and preset["addons-presets"]["published-ids"]:
                    mods = {self.__get_mod(mod) for mod in preset["addons-presets"]["published-ids"]['id']}
                self._presets.add(Preset(name, preset["addons-presets"]["last-update"], list(mods)))
        except KeyError:
            self._presets = set()
        unused_preset = {preset for preset in self._presets if preset.name == UNUSED_TAG}
        if unused_preset:
            self._presets.remove(unused_preset.pop())
        

    def __get_mod(self, id: str) -> Mod | None:
        for mod in self._mods:
            if mod.steam_id == id:
                return mod
        return None
    
    def get_unused_mods(self) -> [Mod]:
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
        