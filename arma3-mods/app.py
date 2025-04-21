import os
from launcher import Arma3Launcher
import argparse


DEFAULT_PATH: str=os.environ.get("LOCALAPPDATA") + "/Arma 3 Launcher" # type: ignore



def main():
    parser = argparse.ArgumentParser(description='Arma 3 Launcher presets helper')
    parser.add_argument('-p', '--path', help='Path to Arma 3 launcher data folder (default is in %%LOCALAPPDATA%%/Arma 3 Launcher)', default=DEFAULT_PATH)
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    # subparsers.required = True

    mods_parser = subparsers.add_parser('mods', help='List steam mods.')
    mods_parser.add_argument('--unused', action='store_true', help='Only show unused mods')

    presets_parser = subparsers.add_parser('preset', help='List, inspect or create a preset with unused mods.')
    presets_subparsers = presets_parser.add_subparsers(dest='preset_command', help='Available commands')
    # presets_subparsers.required = True

    presets_inspect_parser = presets_subparsers.add_parser('inspect', help='Prints the mods of a specified preset')
    presets_inspect_parser.add_argument('preset_name', help='Name of the preset')

    presets_subparsers.add_parser('create', help='Creates a preset from unused mods')
    presets_subparsers.add_parser('list', help='List all presets')
    # presets_create_parser.add_argument('preset_name', help='Name of the preset')

    args = parser.parse_args()

    launcher = Arma3Launcher(args.path)

    # TODO: Proper recator with modularization of commands sub-menus

    if args.command == 'mods':
        mods = launcher.mods
        if args.unused:
            mods = launcher.get_unused_mods()
        for mod in mods:
            print(mod.name)
    elif args.command == 'preset':
        if args.preset_command == 'list':
            for preset in launcher.presets:
                print(preset.name)
        elif args.preset_command == 'inspect':
            preset = next((preset for preset in launcher.presets if preset.name == args.preset_name), None)
            if preset:
                for mod in preset.mods:
                    print(mod.name)
            else:
                print(f"Preset '{args.preset_name}' not found")
        elif args.preset_command == 'create':
            launcher.make_unused_preset()
        else:
            presets_parser.print_help()
    
    elif args.command == 'help' or not args.command:
        parser.print_help()

if __name__ == "__main__":
    main()


