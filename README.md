# GameSave Manager to Ludusavi Mapping converter

This script converts GameSave Manager (GSM) backup files into Ludusavi mapping files. [GameSave Manager](https://www.gamesave-manager.com/) (Windows) and [Ludusavi](https://github.com/mtkennerly/ludusavi) (Windows, Linux/Mac) are two game save management tools and this script helps users transition from GSM to Ludusavi and vice-versa. Since GSM only supports Windows, tends to be slower and is closed-source, for universal game save management, the ability to Ludusavi is very useful. On the other hand, Ludusavi seems to be less robust, offer less features, have a more bare-bones GUI and its scanning is, in certain cases, more incomplete, the ability to convert to GSM might also be useful (in development).

## Prerequisites

- Python 3.x installed
- Required Python packages installed: `py7zr`, `win32com`