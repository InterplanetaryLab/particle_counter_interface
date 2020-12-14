from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pydrive.files

class DriveInterface:
    # class variables
    gauth = 0
    drive = 0


    # gets authentication through webbrowser
    def __init__(self):
        self.gauth = GoogleAuth()

    def auth_browser(self):
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)

    # gets authentication through stored credentials file
    def auth_file(self,filename):
        self.gauth = GoogleAuth()
        self.gauth.LoadCredentialsFile(filename)
        self.drive = GoogleDrive(self.gauth)

    # stores auth into a file so that browser verification is not needed
    def save_auth_file(self,filename):
        self.gauth.SaveCredentialsFile(filename)

    # store file into the root directory of the Google Drive User
    def upload_file(self,filename):
        try:
            file = self.drive.CreateFile()
            file.SetContentFile(filename)
            file.Upload()
        except pydrive.files.FileNotUploadedError:
            print("failed to upload file")


    # uploads the specified folder into folder in the root directory (i.e no sub directories)
    def upload_file_folder(self,filename,folder_name):
        try:
            folders = self.drive.ListFile({'q': "trashed=false"}).GetList()
            for folder in folders:
                if folder['title'] == folder_name:
                    print(folder['parents'])
                    file = self.drive.CreateFile({'parents': [{'id': folder['id']}]})
                    file.SetContentFile(filename)
                    file.Upload(param={'supportsTeamDrives': True})
                print(folder['title'])
        except pydrive.files.FileNotUploadedError:
            print("failed to upload file")
