README

---------------------------------------------------------

Author:
Andrew Lopez

Date:
March 25, 2023

Project Title:
Lights GUI

---------------------------------------------------------

Project Description:
Create a GUI to control RGBCW bulbs on a Windows 10 PC.
Developed on a Windows 10 PC with resolution 1920x1080 and six RGBCW light bulbs.

LightsGUI.py contains the main program.
LightsGUI.py can identify devices on the network and allows the user to assign names and groups.
This information is then saved to a 'txt' file in the './devices' directory. This allows the user to easily use the program without having to re-identify the devices.
The txt file is NECESSARY to use the other functions of the program (change color/brightness, etc.).
utils.py contains several functions used by LightsGUI.py

Used flux_led library to control bulbs (https://github.com/Danielhiversen/flux_led).

Used tkinter library to build the gui.

Used pyinstaller to create a one file executable to run on windows.

Device Functions

'Change Colors' -- Required: R (0-255), G (0-255), B (0-255). Optional: Brightness (0-100) percentage. Set the color of the selected devices.

'Set Warm White' -- Optional: Brightness (0-100). Set the color of the selected devices to 'Warm White' (CCT temp 2700).

'Set Cool White' -- Optional: Brightness (0-100). Set the color of the selected devices to 'Cool White' (CCT temp 6500).

'Turn Devices Off' -- Turn the selected devices off. 

'Turn Devices On' -- Turn the selected devices on.

'Change Brightness' -- Required: Brightness (0-100) percentage. Set the brightness of the selected devices.


---------------------------------------------------------

Goals:
The primary goals of this project were
1. To learn how to create a GUI using python,
2. To practice using modules I am unfamiliar with,
3. To gain experience developing a program from beginning to end,
4. To practice general python skills.

---------------------------------------------------------

Usage:
0. If the device information is already saved into the './devices' directory, skip to step 7.

Scan devices and save device information.
1. Please create a 'devices' directory in the program directory.
2. Run the LightsGUI.exe and click 'Device Scanner'
3. Turn on all devices and click 'Scan'
    3.5 For easier identification click the 'Change Device Colors' checkbox. Be aware that this WILL change the colors and brightnesses of all devices found.
4. Make sure all devices were found. If not please click 'Scan' again.
5. (optional) Add names and groups to each device. Enter a filename for the txt file. The default filename is 'DeviceInfo'
6. Click the 'Save Info' button to save the device information into a text file.

Utilize device information file to use devices.

7. Click the 'Change Devices' button.
8. Click the 'Load Devices from File' button to access the txt files in './devices'.
    8.5 If the desired device has availability 'N', please make sure it is powered and click 'Recheck Availability'.
9. Select devices you wish to use via the individual device checkboxes or the Control By Group Menubox.
10. Enter the necessary RGB-Brightness values for the desired function (if applicable)
11. Click the desired function button.

---------------------------------------------------------

Installation:
Install with pyinstaller using the command: 
    $ pyinstaller --noconsole --onefile LightsGUI.py

---------------------------------------------------------

LICENSE/COPYING: 
This project is licensed under the GNU General Public License v3.0 (GNU GPLv3) URL: https://www.gnu.org/licenses/gpl-3.0.en.html 
See LICENSE.md for the full text of the license.
