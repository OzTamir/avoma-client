from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ..models.transcriptions import Transcription


class TranscriptionsAPI:
    """API endpoints for transcriptions."""

    def __init__(self, client):
        self.client = client
        self.client.logger.debug("TranscriptionsAPI initialized")

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
        self.client.logger.debug(
            f"Listing transcriptions from {from_date} to {to_date}"
        )
        if meeting_uuid:
            self.client.logger.debug(f"Filtering by meeting UUID: {meeting_uuid}")

        params = {
            "from_date": from_date,
            "to_date": to_date,
        }

        if meeting_uuid is not None:
            params["meeting_uuid"] = str(meeting_uuid)

        data = await self.client._request("GET", "/transcriptions", params=params)
        transcriptions = [Transcription.model_validate(item) for item in data]
        self.client.logger.debug(f"Retrieved {len(transcriptions)} transcriptions")
        return transcriptions

    async def get(self, uuid: UUID) -> Transcription:
        """Get a single transcription by UUID.

        Args:
            uuid: Transcription UUID

        Returns:
            Transcription details
        """
        self.client.logger.debug(f"Getting transcription with UUID: {uuid}")
        data = await self.client._request("GET", f"/transcriptions/{uuid}")
        transcription = Transcription.model_validate(data)
        self.client.logger.debug(f"Retrieved transcription: {uuid}")
        return transcription
