from pathlib import Path

class Arma3LauncherLocations:
    def __init__(self, path: str | Path) -> None:
        self._root = Path(path)
        pass

    @property
    def root(self) -> Path:
        return self._root

    @property
    def presets(self) -> Path:
        return self._root / "Presets"
    
    @property
    def steam(self) -> Path:
        return self._root / "Steam.json"