from src.external_sources.GoogleDrive import GoogleDriveStorage

if __name__ == "__main__":
    google_drive = GoogleDriveStorage()
    google_drive.login()

    print("Usuário logado:", google_drive.get_user_info())

    files = google_drive.list_files()
    print("Arquivos no Google Drive:")
    for file in files:
        print(f"{file['name']} ({file['id']})")
