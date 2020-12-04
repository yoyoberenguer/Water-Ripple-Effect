# -*- mode: python -*-

block_cipher = None


a = Analysis(['main_rippleEffect.py'],
             pathex=['C:\\Users\\yoann\\PycharmProjects\\RippleEffect\\CythonOpenMP'],
             binaries=[],
             datas=[('*.wav', '.'),
                    ('*.pyd', '.'),
                    ('*.pyx', '.'),
                    ('*.png', '.')
                   ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main_rippleEffect',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir='C:\\Users\\yoann\\AppData\\Local\\Temp\\toto',
          console=True )
