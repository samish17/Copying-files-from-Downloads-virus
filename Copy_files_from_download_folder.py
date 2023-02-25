import pyautogui

import psutil
import os

# Setting the source folder (Download folder from 'C' drive).
source_folder = 'C:/Users\{}\Downloads'.format(os.getlogin())
# Giving a folder name that is created in the USB drive
# as "user's device name + Downloads" e.g. Jack Downloads
parent_folder = 'others'  # parent folder in USB Drive
sub_folder_name = os.getlogin() + ' Downloads'  # sub-folder 1 in USB Drive

try:

    def my_USB():
        """" This function loops through the disks at first, if removable disk is not found the process is the process id
        discontinued,if the removable disk is present, confirmation prompt is initiated to ask user if he/she wants to
        continue the process and """

        # Loop through all connected disks
        # And running a program if removable disk is inserted.
        for disk in psutil.disk_partitions():
            # Check if the disk is a removable drive (i.e. a USB flash drive)
            if 'rw,removable' in disk.opts:
                # print the path of the removable drive
                disk_location = disk.mountpoint
                print('USB flash drive found at:', disk_location)

                # Asking user if he/she really wants to continue
                ask = pyautogui.confirm('The USB is now mounted and do you want to continue?', buttons=['Yes', 'No'])

                # Proceeding the script if permission is granted
                if ask == 'Yes':
                    # importing modules to create folder and to copy files from the device
                    import shutil
                    # defining the location of the created folder in USB
                    parent_folder_location = os.path.join(disk_location, parent_folder)  # folder location for parent
                    # folder location for sub_folder
                    sub_folder_location = '{}\{}'.format(parent_folder_location, sub_folder_name)
                    # Check if the sub_folder already exists
                    if not os.path.exists(sub_folder_location):
                        # If the sub_folder does not exist, create it
                        os.makedirs(sub_folder_location)
                        print('Created subfolder:', sub_folder_location)
                    else:
                        print('Subfolder already exists:', sub_folder_location)

                    # Changing the permissions of the source file (downloads folder) to allow read access
                    os.chmod(source_folder, 0o777)

                    # Iterating through each file in the downloads folder
                    for files in os.listdir(source_folder):
                        # Get the full path of the file
                        source_location = os.path.join(source_folder, files)
                        destination_raw = '{}/{}'.format(parent_folder_location, sub_folder_name)
                        destination_location = os.path.join(destination_raw, files)
                        # exception handling for PermissionError and continuing the further process if error
                        # occurs in the middle of the process
                        try:
                            # Copy the file to the backup folder
                            shutil.copy(source_location, destination_location)
                            print('File {} copied successfully to a {}'.format(files, sub_folder_location))
                        except PermissionError:
                            print("Permission denied and couldn't copy a file: {}".format(files))
                            continue
                    print('Task completed successfully.')
                    pyautogui.alert('Task completed successfully.', button='OK')
                    break
                # Cancelling the process if permission is denied.
                else:
                    pyautogui.alert('Process was cancelled.', button='Close')
                    break

            # Showing alert if removable disk is not inserted.
            # else:
            #     pyautogui.alert('USB is not inserted.', button='OK')
            #     break  # breaking the first 'for loop'
    

    my_USB()

# exception block for unknown error. (backup exception handling)
# except FileExistsError as e:
#     pyautogui.alert("File named '{}' already exists.".format(folder_name), button='OK')
#
except Exception as e:
    pyautogui.alert('Error occurred as: {}'.format(e), button='OK')
