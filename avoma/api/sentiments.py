from typing import Optional
from uuid import UUID

from ..models.sentiments import MeetingSentiment, MeetingSentimentsList, SentimentQuery


class SentimentsAPI:
    """API endpoints for meeting sentiments."""

    def __init__(self, client):
        self.client = client

    async def list(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        status: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> MeetingSentimentsList:
        """List meeting sentiment analyses with optional filters.

        Args:
            from_date: Optional start date-time in ISO format
            to_date: Optional end date-time in ISO format
            status: Optional status to filter by (pending, completed, failed)
            page_size: Number of results per page (max 20)

        Returns:
            Paginated list of meeting sentiment analyses
        """
        query = SentimentQuery(
            from_date=from_date,
            to_date=to_date,
            status=status,
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
            Meeting sentiment analysis details
        """
        data = await self.client._request("GET", f"/sentiments/{meeting_uuid}")
        return MeetingSentiment.model_validate(data)

    async def analyze(self, meeting_uuid: UUID) -> MeetingSentiment:
        """Request sentiment analysis for a meeting.

        Args:
            meeting_uuid: UUID of the meeting to analyze

        Returns:
            Created sentiment analysis request (initially in pending state)
        """
        data = await self.client._request("POST", f"/sentiments/{meeting_uuid}/analyze")
        return MeetingSentiment.model_validate(data)
