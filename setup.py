import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["pygame"], "include_files": ["blocks/", "framework/", "graphs/"]}

base = None
if sys.platform == "win32":
    base = "win32GUI"

setup(name="Pathifinder",
      version="1.4",
      description="My GUI application!",
      options={"build_exe": build_exe_options},
      executables=[Executable("pathfinder.py", base=base)])
