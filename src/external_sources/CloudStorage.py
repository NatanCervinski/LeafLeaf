from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class CloudStorage(ABC):
    """Classe base para serviços de armazenamento na nuvem."""

    def __init__(self: "CloudStorage") -> None:
        self.user_info: Optional[Dict[str, str]] = None  # Informações do usuário

    @abstractmethod
    def login(self: "CloudStorage") -> None:
        pass

    @abstractmethod
    def list_files(self: "CloudStorage") -> List[Dict[str, str]]:
        pass

    def get_user_info(self: "CloudStorage") -> Optional[Dict[str, str]]:
        return self.user_info
