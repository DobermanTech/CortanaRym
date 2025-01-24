# main.spec
# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['C:\\Data\\Custom Programs\\CortanaRym\\Version 0.4'],
    binaries=[],
    datas=[
        ('C:\\Data\\Custom Programs\\CortanaRym\\Version 0.4\\game_data.txt', '.'),
        ('C:\\Data\\Custom Programs\\CortanaRym\\Version 0.4\\weapons.json', '.'),
        ('C:\\Data\\Custom Programs\\CortanaRym\\Version 0.4\\requirements.txt', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main'
)
