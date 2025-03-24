from typing import Optional
from uuid import UUID

from ..models.calls import Call, CallCreate, CallUpdate, CallsList, CallsQuery


class CallsAPI:
    """API endpoints for calls."""

    def __init__(self, client):
        self.client = client

    async def list(
        self,
        from_date: str,
        to_date: str,
        host_email: Optional[str] = None,
        participant_email: Optional[str] = None,
        status: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> CallsList:
        """List calls with optional filters.

        Args:
            from_date: Start date-time in ISO format
            to_date: End date-time in ISO format
            host_email: Optional host email to filter by
            participant_email: Optional participant email to filter by
            status: Optional status to filter by
            page_size: Number of calls per page (max 20)

        Returns:
            Paginated list of calls
        """
        query = CallsQuery(
            from_date=from_date,
            to_date=to_date,
            host_email=host_email,
            participant_email=participant_email,
            status=status,
        )

        params = query.model_dump(exclude_none=True)
        if page_size is not None:
            params["page_size"] = page_size

        data = await self.client._request("GET", "/calls", params=params)
        return CallsList.model_validate(data)

    async def get(self, call_uuid: UUID) -> Call:
        """Get a specific call by UUID.

        Args:
            call_uuid: Call UUID

        Returns:
            Call details
        """
        data = await self.client._request("GET", f"/calls/{call_uuid}")
        return Call.model_validate(data)

    async def create(self, call: CallCreate) -> Call:
        """Create a new call.

        Args:
            call: Call creation data

        Returns:
            Created call
        """
        data = await self.client._request(
            "POST", "/calls", json=call.model_dump(exclude_unset=True)
        )
        return Call.model_validate(data)

    async def update(self, call_uuid: UUID, call: CallUpdate) -> Call:
        """Update an existing call.

        Args:
            call_uuid: UUID of the call to update
            call: Call update data

        Returns:
            Updated call
        """
        data = await self.client._request(
            "PUT", f"/calls/{call_uuid}", json=call.model_dump(exclude_unset=True)
        )
        return Call.model_validate(data)

    async def cancel(self, call_uuid: UUID) -> Call:
        """Cancel a call.

        Args:
            call_uuid: UUID of the call to cancel

        Returns:
            Updated call with cancelled status
        """
        data = await self.client._request("POST", f"/calls/{call_uuid}/cancel")
        return Call.model_validate(data)

    async def start(self, call_uuid: UUID) -> Call:
        """Start a call.

        Args:
            call_uuid: UUID of the call to start

        Returns:
            Updated call with in_progress status
        """
        data = await self.client._request("POST", f"/calls/{call_uuid}/start")
        return Call.model_validate(data)

    async def end(self, call_uuid: UUID) -> Call:
        """End a call.

        Args:
            call_uuid: UUID of the call to end

        Returns:
            Updated call with completed status
        """
        data = await self.client._request("POST", f"/calls/{call_uuid}/end")
        return Call.model_validate(data)
