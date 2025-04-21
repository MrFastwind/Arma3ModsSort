default: build

.PHONY: build

clean:
	rm rf dist build .\arma3-mods\__pycache__ .\arma3-mods\*.spec

build:
	pyinstaller .\arma3-mods\app.py -i NONE --onefile -n arma3mods

run: build
	.\dist\arma3mods.exe