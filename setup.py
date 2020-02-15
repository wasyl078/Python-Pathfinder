import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["pygame"], "include_files": ["blocks/", "framework/", "graphs/"]}

base = None


setup(name="Pathifinder",
      version="1.0",
      description="My GUI application!",
      options={"build_exe": build_exe_options},
      executables=[Executable("pathfinder_v1.py", base=base)])

