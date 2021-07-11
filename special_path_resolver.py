import os
import userpaths
import winreg

def get_steam_installation_path():
    try:

        # 64-bit registry path
        key_64bit = r"SOFTWARE\Wow6432Node\Valve\Steam"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_64bit) as reg_key:
            try:
                value, _ = winreg.QueryValueEx(reg_key, "InstallPath")
                steam_path = os.path.join(value, "steam.exe")
                return steam_path if os.path.exists(steam_path) else None
            except FileNotFoundError:
                pass  # Continue to 64-bit registry path if not found

            
        # 32-bit registry path
        key_32bit = r"SOFTWARE\Valve\Steam"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_32bit) as reg_key:
            try:
                value, _ = winreg.QueryValueEx(reg_key, "InstallPath")
                steam_path = os.path.join(value, "steam.exe")
                return steam_path if os.path.exists(steam_path) else None
            except FileNotFoundError:
                return None  # Steam not found in either registry path


    except Exception as e:
        print(f"ERROR: {e}")
        return None


def resolve_special_path(special_path):
    special_path = special_path.replace("%", "")

    special_paths = {
        "APPDATA": os.environ.get('APPDATA'),
        "LOCALAPPDATA": os.environ.get('LOCALAPPDATA'),
        "APPDATA_LOCAL": os.environ.get('LOCALAPPDATA'),
        "TEMP": os.environ.get('TEMP'),
        "TMP": os.environ.get('TMP'),
        "USERPROFILE": os.environ.get('USERPROFILE'),
        "HOMEPATH": os.path.expanduser('~'),
        "SYSTEMROOT": os.environ.get('SYSTEMROOT'),
        "PROGRAMFILES": os.environ.get('PROGRAMFILES'),
        "COMMONPROGRAMFILES": os.environ.get('COMMONPROGRAMFILES'),
        "COMMONAPPDATA": os.environ.get('COMMONAPPDATA'),
        "PUBLIC": os.environ.get('PUBLIC'),
        "VIDEOS": userpaths.get_my_videos(),
        "PICTURES": userpaths.get_my_pictures(),
        "MUSIC": userpaths.get_my_music(),
        "DOWNLOADS": userpaths.get_downloads(),
        "DESKTOP": userpaths.get_desktop(),
        "DOCUMENTS": userpaths.get_my_documents(),
        "STEAM_CLOUD": get_steam_installation_path(),
        "SAVED_GAMES": os.path.join(os.environ.get('USERPROFILE'), "Saved Games")
    }

    return special_paths.get(special_path)