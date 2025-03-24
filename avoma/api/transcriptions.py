from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ..models.transcriptions import Transcription


class TranscriptionsAPI:
    """API endpoints for transcriptions."""

    def __init__(self, client):
        self.client = client

    async def list(
        self,
        from_date: str,
        to_date: str,
        meeting_uuid: Optional[UUID] = None,
    ) -> List[Transcription]:
        """List transcriptions with optional filters.

        Args:
            from_date: Start date-time in ISO format
            to_date: End date-time in ISO format
            meeting_uuid: Optional meeting UUID to filter by

        Returns:
            List of transcriptions
        """
        params = {
            "from_date": from_date,
            "to_date": to_date,
        }

        if meeting_uuid is not None:
            params["meeting_uuid"] = str(meeting_uuid)

        data = await self.client._request("GET", "/transcriptions", params=params)
        return [Transcription.model_validate(item) for item in data]

    async def get(self, uuid: UUID) -> Transcription:
        """Get a single transcription by UUID.

        Args:
            uuid: Transcription UUID

        Returns:
            Transcription details
        """
        data = await self.client._request("GET", f"/transcriptions/{uuid}")
        return Transcription.model_validate(data)
