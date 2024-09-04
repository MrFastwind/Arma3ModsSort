default: build

build: 
	pyinstaller .\arma3-mods\app.py -i NONE --onefile -n arma3mods

run: build
	.\dist\arma3mods.exe