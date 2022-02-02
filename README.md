<div align="center">
  <img src="https://github.com/alexitx/eternal-radio-player/raw/gui/docs/assets/eternal-radio-player.svg" height="100px"/>

  <h1>Eternal Radio Player</h1>

  <p>A desktop app for the online radio station <a href="https://radio.eternalnetworktm.com">Eternal Radio<a>.
  Provides the ability to listen to the live radio stream and see recently played songs.</p>

  <p><em>This app is experimental, but can be used as an alternative to a web browser on systems
  with limited resources or where a graphical environment is not present.</em></p>
</div>

## Table of contents

- [Installation](#installation)
    - [Windows](#windows)
    - [Linux / Other](#linux--other)
- [Usage](#usage)
    - [Windows](#windows-1)
    - [Linux / Other](#linux--other-1)
- [CLI arguments](#cli-arguments)
- [License](#license)


## Installation

### Windows

Install Python 3.7 or newer if you haven't already. The latest stable 64-bit version from the
[official website][python-download] is strongly recommended over the Microsoft Store.

In case you have issues installing or running the app as a Python package later on, download the
portable version from the [latest release][releases]. Though this is not recommended, as it is
larger and slower.

1. Open Command Prompt or PowerShell

2. Check if your Python version is correct:
    ```
    python --version
    ```

3. Update pip and dependencies:
    ```
    python -m pip install --upgrade pip
    python -m pip install --upgrade setuptools wheel
    ```

4. Install:

    Note: Eternal Radio Player has command-line interface by default.
    You can optionally install the GUI dependencies.

    For GUI installation:
    ```
    python -m pip install --upgrade eternal-radio-player[gui]
    ```
    For minimal (command-line only) installation:
    ```
    python -m pip install --upgrade eternal-radio-player
    ```

5. Update Eternal Radio Player periodically using the previous installation command

### Linux / Other

1. Open a terminal

2. Install the latest stable Python version (3.7 or newer) using your distro's package manager

3. Check if your Python version is correct
    ```sh
    $ python3 --version
    ```

4. Update pip and dependencies
    ```sh
    $ python3 -m pip install --user --upgrade pip
    $ python3 -m pip install --user --upgrade setuptools wheel
    ```

4. Install:

    Note: Eternal Radio Player has command-line interface by default.
    You can optionally install the GUI dependencies.

    For GUI installation:
    ```sh
    $ python3 -m pip install --upgrade eternal-radio-player[gui]
    ```
    For minimal (command-line only) installation:
    ```sh
    $ python3 -m pip install --upgrade eternal-radio-player
    ```

6. Update Eternal Radio Player periodically using the previous installation command


## Usage

### Windows

1. Open Command Prompt or PowerShell

2. Run the command `eternal-radio-player-gui` (or `eternal-radio-player` to leave the shell visible
    for troubleshooting)

    Eternal Radio Player will launch in GUI mode by default if the required libraries are installed
    and available.

    If you get an error about the command not being recognized or missing, run it as a Python
    module instead:
    ```
    python -m eternal_radio_player
    ```

    If that also doesn't work, [add your Python scripts directory to the
    system path][windows-add-python-to-path].

3. (Optional) Create a desktop shortcut with the chosen command from step #2

    You can pin this shortcut to the start menu or task bar.

### Linux / Other

1. Open a terminal

2. Run the command `eternal-radio-player`

    Eternal Radio Player will launch in GUI mode by default if the required libraries are installed
    and available.

    If you get an error about the command not being recognized or missing, run it as a Python
    module instead:
    ```sh
    $ python3 -m eternal_radio_player
    ```

    If that also doesn't work, [add your Python scripts directory to the
    system path][linux-add-python-to-path].

3. (Optional) [Create a desktop shortcut][linux-desktop-shortcut] with the chosen command from
    step #2

Note: If you have issues on Wayland, try running the app with the environment variable set
`QT_QPA_PLATFORM=xcb` to force X11 mode. Example:
```sh
$ QT_QPA_PLATFORM=xcb eternal-radio-player
```


## CLI arguments

| Argument     | Type | Description                    |
|--------------|------|--------------------------------|
| -d, --debug  | bool | Set logging verbosity to debug |
| -c, --cli    | bool | Run in CLI mode                |
| -l, --log    | str  | Log file path                  |
| -C, --config | str  | Config file path               |


## License

GNU General Public License v3.0 or later. See [LICENSE][license] for more information.


[releases]: https://github.com/alexitx/eternal-radio-player/releases
[license]: https://github.com/alexitx/eternal-radio-player/blob/master/LICENSE
[python-download]: https://www.python.org/downloads
[windows-add-python-to-path]: https://superuser.com/a/1558227
[linux-add-python-to-path]: https://stackoverflow.com/a/62823029
[linux-desktop-shortcut]: https://askubuntu.com/a/182717
