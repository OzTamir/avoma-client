from datetime import datetime
from typing import Optional, List
from uuid import UUID
from urllib.parse import urlparse, parse_qs

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
        follow_pagination: bool = False,
        from_page: Optional[int] = None,
        to_page: Optional[int] = None,
    ) -> MeetingList:
        """List meetings with optional filters.

        Args:
            from_date: Start date-time in ISO format
            to_date: End date-time in ISO format
            page_size: Number of records per page (max 100)
            is_call: Filter for voice calls
            is_internal: Filter for internal meetings
            recording_duration__gte: Minimum recording duration
            follow_pagination: If True, will fetch all pages
            from_page: Start from this page number (1-based)
            to_page: Stop at this page number (inclusive)

        Returns:
            Paginated list of meetings. If follow_pagination is True or page range is specified,
            will contain all meetings from the requested pages.
        """
        self.client.logger.debug(f"Listing meetings from {from_date} to {to_date}")
        params = {
            "from_date": from_date,
            "to_date": to_date,
            "page_size": page_size or 100,  # Use max page size if not specified
        }

        if is_call is not None:
            params["is_call"] = str(is_call).lower()
        if is_internal is not None:
            params["is_internal"] = str(is_internal).lower()
        if recording_duration__gte is not None:
            params["recording_duration__gte"] = recording_duration__gte

        # Determine the starting page
        current_page = from_page if from_page else 1

        # Only include page parameter if we're not starting from page 1
        first_params = params.copy()
        if current_page > 1:
            first_params["page"] = current_page

        # Get first page
        data = await self.client._request("GET", "meetings", params=first_params)
        meeting_list = MeetingList.model_validate(data)
        self.client.logger.debug(f"Retrieved {len(meeting_list.results)} meetings")

        # Determine if we should continue fetching pages
        should_continue = (follow_pagination and meeting_list.next) or (
            to_page and current_page < to_page
        )

        if should_continue:
            all_results = meeting_list.results
            total_count = (
                meeting_list.count
            )  # Keep track of total count from first response
            current_page += 1

            while meeting_list.next and (not to_page or current_page <= to_page):
                # Add page parameter for subsequent requests
                params_with_page = params.copy()
                params_with_page["page"] = current_page

                data = await self.client._request(
                    "GET", "meetings", params=params_with_page
                )
                meeting_list = MeetingList.model_validate(data)
                all_results.extend(meeting_list.results)
                self.client.logger.debug(
                    f"Retrieved {len(meeting_list.results)} more meetings"
                )
                current_page += 1

                # Stop if we've reached the end and we're not following pagination
                if not follow_pagination and not to_page:
                    break

            # Create a new MeetingList with all results
            has_more = meeting_list.next is not None and (
                to_page is None or current_page <= to_page
            )
            meeting_list = MeetingList(
                count=total_count,  # Use the total count from first response
                next=meeting_list.next if has_more else None,
                previous=None,
                results=all_results,
            )

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
