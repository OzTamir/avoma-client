from datetime import datetime
from typing import Optional
from uuid import UUID

from ..models.meetings import Meeting, MeetingInsights, MeetingList, MeetingSentiment


class MeetingsAPI:
    """API endpoints for meetings."""

    def __init__(self, client):
        self.client = client
        self.client.logger.debug("MeetingsAPI initialized")

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
        self.client.logger.debug(f"Listing meetings from {from_date} to {to_date}")
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
        meeting_list = MeetingList.model_validate(data)
        self.client.logger.debug(f"Retrieved {len(meeting_list.results)} meetings")
        return meeting_list

    async def get(self, uuid: UUID) -> Meeting:
        """Get a single meeting by UUID.

        Args:
            uuid: Meeting UUID

        Returns:
            Meeting details
        """
        self.client.logger.debug(f"Getting meeting with UUID: {uuid}")
        data = await self.client._request("GET", f"meetings/{uuid}")
        meeting = Meeting.model_validate(data)
        self.client.logger.debug(f"Retrieved meeting: {meeting.subject}")
        return meeting

    async def get_insights(self, uuid: UUID) -> MeetingInsights:
        """Get insights for a meeting.

        Args:
            uuid: Meeting UUID

        Returns:
            Meeting insights including AI notes and keywords
        """
        self.client.logger.debug(f"Getting insights for meeting with UUID: {uuid}")
        data = await self.client._request("GET", f"meetings/{uuid}/insights")
        insights = MeetingInsights.model_validate(data)
        self.client.logger.debug(f"Retrieved insights for meeting: {uuid}")
        return insights

    async def get_sentiments(self, uuid: UUID) -> MeetingSentiment:
        """Get sentiment analysis for a meeting.

        Args:
            uuid: Meeting UUID

        Returns:
            Meeting sentiment analysis
        """
        self.client.logger.debug(f"Getting sentiments for meeting with UUID: {uuid}")
        data = await self.client._request(
            "GET", "meeting_sentiments", params={"uuid": str(uuid)}
        )
        # Check if data is a list and take the first item if it is
        if isinstance(data, list) and data:
            data = data[0]
        sentiment = MeetingSentiment.model_validate(data)
        self.client.logger.debug(f"Retrieved sentiments for meeting: {uuid}")
        return sentiment

    async def drop(self, uuid: UUID) -> dict:
        """Drop a meeting.

        Args:
            uuid: Meeting UUID

        Returns:
            Response message
        """
        self.client.logger.debug(f"Dropping meeting with UUID: {uuid}")
        response = await self.client._request("POST", f"meetings/{uuid}/drop/")
        self.client.logger.debug(f"Meeting {uuid} dropped")
        return response
