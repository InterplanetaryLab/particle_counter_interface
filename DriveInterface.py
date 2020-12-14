from __future__ import print_function
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload

# needs a credentials.json file to start

class DriveInterface:
    # class variables
    drive = 0
    store = 0
    
    MIMETYPEJPG = "image/jpeg"
    MIEMTYPETEXTPLAIN = "text/plain"

    # gets authentication through web browser unless a storage.json file is present
    def __init__(self):
        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = file.Storage('storage.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.drive = discovery.build('drive', 'v3', http=creds.authorize(Http()))

    # prints root directory
    def print_root_directory(self):
        files = self.drive.files().list().execute().get('files', [])
        for f in files:
                print(f['name'],f['mimeType'])
        return files

    # only uploads to root folders but will work with folders that are shortcuts
    def uploadFile(self, filename, cloud_path, mimeType):
        files = self.print_root_directory()
        file_metadata = 0
        for folder in files:
            if folder["name"] == cloud_path and (folder["mimeType"] == "application/vnd.google-apps.shortcut" or folder["mimeType"] == "application/vnd.google-apps.folder"):
                if folder["mimeType"] == "application/vnd.google-apps.shortcut":
                    shortcuts = self.drive.files().list(q= "mimeType='application/vnd.google-apps.shortcut'",fields='*',includeItemsFromAllDrives=True,supportsAllDrives=True).execute().get('files',[])
                    for shortcut in shortcuts:
                        if shortcut['name'] == cloud_path:
                            print(shortcut['shortcutDetails'])
                    file_metadata = {'name' : filename, 'parents': [shortcut['shortcutDetails']['targetId']]}
                else:
                    file_metadata = {'name' : filename, 'parents': [folder['id']]}
                media = MediaFileUpload(filename, mimetype=mimeType,resumable=True)
                file = self.drive.files().create(body=file_metadata,media_body=media,fields='id', supportsAllDrives = True).execute()
                break
