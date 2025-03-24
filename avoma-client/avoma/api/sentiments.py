from typing import Optional
from uuid import UUID

from ..models.sentiments import MeetingSentiment, MeetingSentimentsList, SentimentsQuery


class SentimentsAPI:
    """API endpoints for meeting sentiments."""

    def __init__(self, client):
        self.client = client

    async def list(
        self,
        from_date: str,
        to_date: str,
        meeting_uuid: Optional[UUID] = None,
        page_size: Optional[int] = None,
    ) -> MeetingSentimentsList:
        """List meeting sentiments with optional filters.

        Args:
            from_date: Start date-time in ISO format
            to_date: End date-time in ISO format
            meeting_uuid: Optional meeting UUID to filter by
            page_size: Number of sentiments per page (max 20)

        Returns:
            Paginated list of meeting sentiments
        """
        query = SentimentsQuery(
            from_date=from_date,
            to_date=to_date,
            meeting_uuid=meeting_uuid,
        )

        params = query.model_dump(exclude_none=True)
        if page_size is not None:
            params["page_size"] = page_size

        data = await self.client._request("GET", "/sentiments", params=params)
        return MeetingSentimentsList.model_validate(data)

    async def get(self, meeting_uuid: UUID) -> MeetingSentiment:
        """Get sentiment analysis for a specific meeting.

        Args:
            meeting_uuid: Meeting UUID

        Returns:
            Meeting sentiment analysis
        """
        data = await self.client._request("GET", f"/sentiments/{meeting_uuid}")
        return MeetingSentiment.model_validate(data)
