# key-remapper
A system service that allows you to remap key presses, allowing for complex keybindings systemwide

Prerrequisites:

`python3-evdev`

Non-root users have to be in the `input` group to be able to scan integrated laptop keyboards.

Substitute `SCRIPT_PATH` with the absolute path to `src/key_remapper.py` in `key_remapper.service`.

Copy `key_remapper.service` to `/etc/systemd/system/key_remapper.service`.
