from cx_Freeze import setup, Executable
import sys

buildOptions = dict(packages = [],  # 1
	excludes = [])

exe = [Executable("pg.py")]

# 3
setup(
    name='Test Application',
    version = '0.1',
    author = "IML",
    description = "I'M IML!",
    options = dict(build_exe = buildOptions),
    executables = exe
)
