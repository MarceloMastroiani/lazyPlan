from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid


class Status(str, Enum):
    CRUDA      = "cruda"
    ACTIVA     = "activa"
    PAUSADA    = "pausada"
    DESCARTADA = "descartada"


STATUS_LABELS = {
    Status.CRUDA:      "🟡 Cruda",
    Status.ACTIVA:     "🟢 Activa",
    Status.PAUSADA:    "⚪ Pausada",
    Status.DESCARTADA: "🔴 Descartada",
}


@dataclass
class Project:
    title:       str
    id:          str       = field(default_factory=lambda: str(uuid.uuid4())[:8])
    description: str       = ""
    stack:       list[str] = field(default_factory=list)
    status:      Status    = Status.CRUDA
    links:       list[str] = field(default_factory=list)
    github_url:  str       = ""
    folder_path: str       = ""
    created_at:  str       = field(default_factory=lambda: datetime.now().isoformat())
    updated_at:  str       = field(default_factory=lambda: datetime.now().isoformat())

    def touch(self):
        self.updated_at = datetime.now().isoformat()

    @property
    def stack_str(self) -> str:
        return ", ".join(self.stack) if self.stack else "—"

    @property
    def status_label(self) -> str:
        return STATUS_LABELS.get(self.status, self.status)
