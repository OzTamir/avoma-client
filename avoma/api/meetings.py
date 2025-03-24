from datetime import datetime
from typing import Optional
from uuid import UUID

from ..models.meetings import Meeting, MeetingInsights, MeetingList, MeetingSentiment


class MeetingsAPI:
    """API endpoints for meetings."""

    def __init__(self, client):
        self.client = client

    async def list(
        self,
        from_date: str,
        to_date: str,
        page_size: Optional[int] = None,
        is_call: Optional[bool] = None,
        is_internal: Optional[bool] = None,
        recording_duration__gte: Optional[float] = None,
    ) -> MeetingList:
        """List meetings with optional filters.

        Args:
            from_date: Start date-time in ISO format
            to_date: End date-time in ISO format
            page_size: Number of records per page
            is_call: Filter for voice calls
            is_internal: Filter for internal meetings
            recording_duration__gte: Minimum recording duration

        Returns:
            Paginated list of meetings
        """
        params = {
            "from_date": from_date,
            "to_date": to_date,
        }

        if page_size is not None:
            params["page_size"] = page_size
        if is_call is not None:
            params["is_call"] = is_call
        if is_internal is not None:
            params["is_internal"] = is_internal
        if recording_duration__gte is not None:
            params["recording_duration__gte"] = recording_duration__gte

        data = await self.client._request("GET", "meetings", params=params)
        return MeetingList.model_validate(data)

    async def get(self, uuid: UUID) -> Meeting:
        """Get a single meeting by UUID.

        Args:
            uuid: Meeting UUID

        Returns:
            Meeting details
        """
        data = await self.client._request("GET", f"meetings/{uuid}")
        return Meeting.model_validate(data)

    async def get_insights(self, uuid: UUID) -> MeetingInsights:
        """Get insights for a meeting.

        Args:
            uuid: Meeting UUID

        Returns:
            Meeting insights including AI notes and keywords
        """
        data = await self.client._request("GET", f"meetings/{uuid}/insights")
        return MeetingInsights.model_validate(data)

    async def get_sentiments(self, uuid: UUID) -> MeetingSentiment:
        """Get sentiment analysis for a meeting.

        Args:
            uuid: Meeting UUID

        Returns:
            Meeting sentiment analysis
        """
        data = await self.client._request(
            "GET", "meeting_sentiments", params={"uuid": str(uuid)}
        )
        # Check if data is a list and take the first item if it is
        if isinstance(data, list) and data:
            data = data[0]
        return MeetingSentiment.model_validate(data)

    async def drop(self, uuid: UUID) -> dict:
        """Drop a meeting.

        Args:
            uuid: Meeting UUID

        Returns:
            Response message
        """
        return await self.client._request("POST", f"meetings/{uuid}/drop/")
