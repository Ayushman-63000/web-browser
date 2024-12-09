import sys
from cx_Freeze import setup, Executable

# Base for a GUI application
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Icon path
icon_path = "icon.ico"

# Build options
build_exe_options = {
    "packages": ["PyQt5", "PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWebEngineWidgets"],
    "excludes": [],
    "include_files": [icon_path]  # Include the icon file
}

# Executable options
executables = [
    Executable("new_browser.py", base=base, icon=icon_path)
]

# Setup configuration
setup(
    name="Browser",
    version="0.1",
    description="A Fast and private browser application",
    options={"build_exe": build_exe_options},
    executables=executables
)