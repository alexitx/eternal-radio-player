<div align="center">
  <img src="https://github.com/alexitx/eternal-radio-player/raw/master/docs/assets/eternal-radio-player.svg" height="100px"/>

  <h1>Eternal Radio Player</h1>

  <p>Десктоп приложение за онлайн радио станцията <a href="https://radio.eternalnetworktm.com">Eternal Radio<a>.
  Предоставя възможност за слушане на радио потока на живо и преглед на последно излъчваните песни.</p>

  <p><em>Това приложение е експериментално, но може да се използва като алтернатива на уеб браузър
  на системи с лимитирани ресурси или без графична среда.</em></p>
</div>


## Език
- [Български][readme-bg]
- [English][readme-en]


## Съдържание

- [Инсталация](#инсталация)
    - [Windows](#windows)
    - [Linux / Други](#linux--други)
- [Използване](#използване)
    - [Windows](#windows-1)
    - [Linux / Други](#linux--други-1)
- [CLI аргументи](#cli-аргументи)
- [Лиценз](#лиценз)


## Инсталация

### Windows

Инсталирайте Python 3.7 или по-нова версия, ако все още не сте го направили. Последната стабилна
64-битова версия от [официалния уебсайт][python-download] се препоръчва силно пред версията от
Магазинa на Microsoft

В случай, че имате проблеми с инсталацията или стартиране на приложението като Python пакет
по-късно, свалете преносимата версия от [последния релийс][releases]. По принцип това не се
препоръчва, тъй като тя е по-голяма и по-бавна.

1. Отворете Команден Прозорец (Command Prompt) или PowerShell

2. Проверете дали вашата Python версия е правилна:
    ```
    python --version
    ```

3. Обновете pip и основните пакети:
    ```
    python -m pip install --upgrade pip
    python -m pip install --upgrade setuptools wheel
    ```

4. Инсталирайте

    Бележка: Eternal Radio Player се инсталира с команден интерфейс по подразбиране.
    По желание можете да инсталирате необходимите пакети за графичен интерфейс.

    За инсталация с графичен интерфейс:
    ```
    python -m pip install --upgrade eternal-radio-player[gui]
    ```
    За минимална инсталация (само с команден интерфейс):
    ```
    python -m pip install --upgrade eternal-radio-player
    ```

5. Актуализирайте Eternal Radio Player периодично, като използвате избраната по-горе
команда за инсталация

### Linux / Други

1. Отворете терминал

2. Инсталирайте последната стабилна версия на Python (3.7 или по-нова) чрез пакетния мениджър
на вашата дистрибуция

3. Проверете дали вашата Python версия е правилна:
    ```sh
    $ python3 --version
    ```

4. Инсталирайте библиотеката PortAudio

    За дистрибуции базирани на Debian (Ubuntu, Mint, Pop!_OS, и други):
    ```sh
    sudo apt update && sudo apt install -y libportaudio2
    ```

    За дистрибуции базирани на Arch (Manjaro, EndeavourOS, и други):
    ```sh
    sudo pacman -Syy && sudo pacman -S portaudio
    ```

    Ако не сте сигурни, потърсете онлайн как да инсталирате portaudio на вашата система.

5. Обновете pip и основните пакети:
    ```sh
    $ python3 -m pip install --user --upgrade pip
    $ python3 -m pip install --user --upgrade setuptools wheel
    ```

6. Инсталирайте

    Бележка: Eternal Radio Player се инсталира с команден интерфейс по подразбиране.
    По желание можете да инсталирате необходимите пакети за графичен интерфейс.

    За инсталация с графичен интерфейс:
    ```sh
    $ python3 -m pip install --upgrade eternal-radio-player[gui]
    ```
    За минимална инсталация (само с команден ред):
    ```sh
    $ python3 -m pip install --upgrade eternal-radio-player
    ```

7. Актуализирайте Eternal Radio Player периодично, като използвате избраната по-горе
команда за инсталация


## Използване

### Windows

1. Отворете Команден Прозорец (Command Prompt) или PowerShell

2. Изпълнете командата `eternal-radio-player-gui` (или само `eternal-radio-player`, за да оставите
прозореца видим с цел отстраняване на проблеми)

    Eternal Radio Player ще се стартира с графичен интерфейс по подразбиране, ако необходимите
    библиотеки са инсталирани и налични.

    Ако получите грешка, че командата не е разпозната или не съществува, изпълнете го като
    Python модул:
    ```
    python -m eternal_radio_player
    ```

    Ако все още възниква грешка, [добавете вашата директория за Python скриптове
    към системния път][windows-add-python-to-path].

3. (По желание) Създайте пряк път на работния плот, сочещ към командата от стъпка #2

    Можете да закачите прекия път към старт менюто или лентата на задачите.

### Linux / Други

1. Отворете терминал

2. Изпълнете командата `eternal-radio-player`

    Eternal Radio Player ще се стартира с графичен интерфейс по подразбиране, ако необходимите
    библиотеки са инсталирани и налични.

    Ако получите грешка, че командата не е разпозната или не съществува, изпълнете го като
    Python модул:
    ```sh
    $ python3 -m eternal_radio_player
    ```

    Ако все още възниква грешка, [добавете вашата директория за Python скриптове
    към системния път][linux-add-python-to-path].

3. (По желание) [Създайте пряк път на работния плот][linux-desktop-shortcut],
сочещ към командата от стъпка #2

Бележка: Ако имате проблеми на Wayland, стартирайте приложението с променливата
`QT_QPA_PLATFORM=xcb` за принудително използване на X11 режим. Пример:
```sh
$ QT_QPA_PLATFORM=xcb eternal-radio-player
```


## CLI аргументи

| Аргумент     | Тип  | Описание                               |
|--------------|------|----------------------------------------|
| -d, --debug  | bool | Увеличаване на многословността на лога |
| -c, --cli    | bool | Стартиране с команден ред              |
| -l, --log    | str  | Файлов път за лог                      |
| -C, --config | str  | Файлов път за конфигурация             |


## Лиценз

GNU General Public License v3.0 или по-нов. Вижте [LICENSE][license] за повече информация.


[readme-en]: https://github.com/alexitx/eternal-radio-player/blob/master/README.md
[readme-bg]: https://github.com/alexitx/eternal-radio-player/blob/master/README.bg.md
[releases]: https://github.com/alexitx/eternal-radio-player/releases
[license]: https://github.com/alexitx/eternal-radio-player/blob/master/LICENSE
[python-download]: https://www.python.org/downloads
[windows-add-python-to-path]: https://superuser.com/a/1558227
[linux-add-python-to-path]: https://stackoverflow.com/a/62823029
[linux-desktop-shortcut]: https://askubuntu.com/a/182717
