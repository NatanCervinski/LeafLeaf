import os
from typing import Dict, List, Optional

from google.auth.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import (
    Credentials as OAuth2Credentials,
)
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.external_sources.CloudStorage import CloudStorage


class GoogleDriveStorage(CloudStorage):
    """Implementação do CloudStorage para Google Drive."""

    SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
    TOKEN_PATH = "token.json"
    CREDENTIALS_PATH = "credentials_google_drive.json"

    def __init__(self: "GoogleDriveStorage") -> None:
        super().__init__()
        self.creds: Optional[Credentials] = None
        self.service = None

    def login(self: "GoogleDriveStorage") -> None:
        """Realiza login no Google Drive e salva as credenciais."""
        if os.path.exists(self.TOKEN_PATH):
            self.creds = OAuth2Credentials.from_authorized_user_file(self.TOKEN_PATH)

        if not self.creds or not self.creds.valid:
            if isinstance(self.creds, OAuth2Credentials) and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_PATH, self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            if isinstance(self.creds, OAuth2Credentials):
                with open(self.TOKEN_PATH, "w") as token:
                    token.write(self.creds.to_json())

        if self.creds:
            self.service = build("drive", "v3", credentials=self.creds)
            self._fetch_user_info()

    def _fetch_user_info(self: "GoogleDriveStorage") -> None:
        """Busca informações do usuário logado no Google Drive."""
        try:
            if self.service:
                user_info_service = (
                    self.service.about().get(fields="user(emailAddress)").execute()
                )
                email = user_info_service.get("user", {}).get(
                    "emailAddress", "Desconhecido"
                )
                self.user_info = {"service": "Google Drive", "email": email}
        except Exception as e:
            print(f"Erro ao buscar informações do usuário: {e}")

    def list_files(self: "GoogleDriveStorage") -> List[Dict[str, str]]:
        if not self.service:
            print("Usuário não está logado.")
            return []

        results = (
            self.service.files().list(pageSize=10, fields="files(id, name)").execute()
        )
        return results.get("files", [])
