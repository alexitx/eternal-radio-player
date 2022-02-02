# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'timeago.locales.ar',
        'timeago.locales.bg',
        'timeago.locales.ca',
        'timeago.locales.da',
        'timeago.locales.de',
        'timeago.locales.el',
        'timeago.locales.en_short',
        'timeago.locales.en',
        'timeago.locales.es',
        'timeago.locales.eu',
        'timeago.locales.fa_IR',
        'timeago.locales.fi',
        'timeago.locales.fr',
        'timeago.locales.gl',
        'timeago.locales.guj_IN',
        'timeago.locales.he',
        'timeago.locales.hu',
        'timeago.locales.in_BG',
        'timeago.locales.in_HI',
        'timeago.locales.in_ID',
        'timeago.locales.is',
        'timeago.locales.it',
        'timeago.locales.ja',
        'timeago.locales.ko',
        'timeago.locales.lt',
        'timeago.locales.ml',
        'timeago.locales.my',
        'timeago.locales.nb_NO',
        'timeago.locales.nl',
        'timeago.locales.nn_NO',
        'timeago.locales.pl',
        'timeago.locales.pt_BR',
        'timeago.locales.pt_PT',
        'timeago.locales.ro',
        'timeago.locales.ru',
        'timeago.locales.sv_SE',
        'timeago.locales.ta',
        'timeago.locales.th',
        'timeago.locales.tr',
        'timeago.locales.uk',
        'timeago.locales.vi',
        'timeago.locales.zh_CN',
        'timeago.locales.zh_TW'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='eternal-radio-player',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icons/eternal-radio-player.ico'
)
