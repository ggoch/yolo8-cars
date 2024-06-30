import os

def rename_folder(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        print(f"Folder renamed from '{old_name}' to '{new_name}' successfully.")
    except FileNotFoundError:
        print(f"The folder '{old_name}' does not exist.")
    except PermissionError:
        print(f"Permission denied to rename the folder '{old_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")