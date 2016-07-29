from cx_Freeze import setup, Executable

setup(
    name = 'vk_users_parser',
    version = '0.1',
    description = 'Parsing users from groups',
    executables = [Executable(vk_users_parser.py)]
)