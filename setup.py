import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

    setup(
        name='br.com.bluefocus.printhandler',
        version='0.0.1',
        packages=['host/windows'],
        url='http://www.bluefocus.com.br',
        license='',
        author='Ronaldo Mota Geraldino',
        author_email='ronaldomg@gmail.com',
        description='Print Helper for non NPAPI',
        options = {"build_exe": build_exe_options},
        executables = [Executable("printhost", base=base)])

else:
    from distutils.core import setup

    setup(
        name='br.com.bluefocus.printhandler',
        version='0.0.1',
        packages=['host/linux'],
        url='http://www.bluefocus.com.br',
        license='',
        author='Ronaldo Mota Geraldino',
        author_email='ronaldomg@gmail.com',
        description='Print Helper for non NPAPI'
    )
