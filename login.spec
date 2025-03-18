# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\controle_de_volumes\\src\\login.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\controle_de_volumes\\Banco', 'Banco/'), ('D:\\controle_de_volumes\\Banco\\database.py', '.'), ('D:\\controle_de_volumes\\Doc', 'Doc/'), ('D:\\controle_de_volumes\\Doc\\README.md', '.'), ('D:\\controle_de_volumes\\Doc\\requirements.txt', '.'), ('D:\\controle_de_volumes\\Doc\\utils.py', '.'), ('D:\\controle_de_volumes\\etiquetas', 'etiquetas/'), ('D:\\controle_de_volumes\\img', 'img/'), ('D:\\controle_de_volumes\\img\\baixados.jpg', '.'), ('D:\\controle_de_volumes\\img\\instagramC.jpg', '.'), ('D:\\controle_de_volumes\\img\\libelula_ico.ico', '.'), ('D:\\controle_de_volumes\\img\\libelulaP.jpg', '.'), ('D:\\controle_de_volumes\\img\\OIP.jpeg', '.'), ('D:\\controle_de_volumes\\img\\user.jpg', '.'), ('D:\\controle_de_volumes\\relatorios', 'relatorios/'), ('D:\\controle_de_volumes\\src', 'src/'), ('D:\\controle_de_volumes\\src\\login.py', '.'), ('D:\\controle_de_volumes\\src\\main.py', '.'), ('D:\\controle_de_volumes\\src\\tab_feira.py', '.'), ('D:\\controle_de_volumes\\src\\tab_loja.py', '.'), ('D:\\controle_de_volumes\\src\\tab_usuario.py', '.'), ('D:\\controle_de_volumes\\src\\tab_volumes.py', '.'), ('D:\\controle_de_volumes\\src\\TabRelatorio.py', '.'), ('D:\\controle_de_volumes\\ui', 'ui/'), ('D:\\controle_de_volumes\\ui\\login.ui', '.'), ('D:\\controle_de_volumes\\ui\\main.ui', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='login',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\controle_de_volumes\\img\\libelula_ico.ico'],
)
