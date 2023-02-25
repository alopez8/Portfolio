README


Project:
GetThatCatnipCoots!.py
author: Andrew Lopez
Date started (mm/dd/yyyy): 02-16-2023
Date finished (mm/dd/yyyy): 02-25-2023


Description:
This is a simple game made for the Ludwig Jam 2023 on itch.io (https://itch.io/jam/ludwig-2023)

GetThatCatnipCoots is a text-based adventure game in which the player helps Coots the cat get catnip in the kitchen. This is done by giving Coots a command and optionally an object e.g. 'look' (for look around your area) or 'look catnip' (for look around the catnip).

This project was made entirely by the author using python 3.11.1 and pygame.

The rules for the jam are as follows:
    1. Games must be safe for streaming (no DMCA music or TOS violations).
    2. Games must be made entirely within the time frame.
    3. Games can be made using any language, game engine, or free assets.
    4. No more than 4 people to a team (ask in the community tab for exceptions).
    5. Games must be submitted to a public GitHub repository.

This project was inspired by the browser game "Don't Shit Your Pants" by Teddy Lee and Kenny Lee for Cellar Door Games.

Credits:
Three assets created by others were used under Creative Commons licenses. No modifications were made to these assets.
Sound Effects: 'And The Winner Is' and 'Total Fail' by congusbongus. Both available for use under the CC0 (https://creativecommons.org/publicdomain/zero/1.0/) at (https://opengameart.org/content/and-the-winner-is and https://opengameart.org/content/total-fail)
Font: 'AC437 IBM VGA 8x16' by VileR (Website: https://int10h.org/oldschool-pc-fonts/). Available for use under the CC BY-SA 4.0 license (https://creativecommons.org/licenses/by-sa/4.0/).


Installation Instructions (Windows10): 
Download 'GetThatCatnipCoots!.py, the 'sounds' folder, and the 'fonts' folder. Store all three should be in the same directory.
The 'sounds' folder should contain two files: 
1. andthewinneris_congusbongus.ogg
2. totalfail_congusbongus.ogg

The 'fonts'folder should contain one file:
1. Ac437_IBM_VGA_8x16.ttf

Install with pyinstaller using the command:
$ pyinstaller -w --add-data 'sounds;./sounds' --add-data 'fonts;./fonts' GetThatCatnipCoots!.py

The executable GetThatCatnipCoots!.exe will be in the './dist/GetThatCatnipCoots!' directory

LICENSE/COPYING:
This project is licensed under the GNU General Public License v3.0 (GNU GPLv3) URL: https://www.gnu.org/licenses/gpl-3.0.en.html
See COPYING.md for the full text of the license.