import re
from pydantic import BaseModel, field_validator

class SectorRequest(BaseModel):
    """Model representing a sector request with validation."""
    sector: str

    @field_validator('sector')
    @classmethod
    def validate_sector(cls, v: str) -> str:
        """Validate sector string."""
        if len(v) < 3:
            raise ValueError("Sector must be at least 3 characters long")
        if len(v) > 50:
            raise ValueError("Sector cannot exceed 50 characters")
        if not re.match(r"^[A-Za-z\s]+$", v):
            raise ValueError("Sector must only contain letters and spaces")
        return v
