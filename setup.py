from cx_Freeze import setup, Executable

includefiles = ['blocks/', 'boards/', 'general/', 'graphs/', 'pictures/']
includes = []
excludes = ['numpy', 'test', 'tkinter']
packages = ['pygame']

setup(
    name='Python Pathfinder',
    version='0.1',
    description='Two player bomberman like game',
    author='Wasyl',
    author_email='wasilewski078@gmail.com',
    options={'build_exe': {'includes': includes, 'excludes': excludes, 'packages': packages, 'include_files': includefiles}},
    executables=[Executable('pathfinder.py')]
)
