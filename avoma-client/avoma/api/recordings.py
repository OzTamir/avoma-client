from uuid import UUID
from ..models.recordings import Recording


class RecordingsAPI:
    """API endpoints for recordings."""

    def __init__(self, client):
        self.client = client

    async def get_by_meeting(self, meeting_uuid: UUID) -> Recording:
        """Get recording by meeting UUID.

        Args:
            meeting_uuid: Meeting UUID

        Returns:
            Recording details including download URLs
        """
        data = await self.client._request(
            "GET", "/recordings", params={"meeting_uuid": str(meeting_uuid)}
        )
        return Recording.model_validate(data)

    async def get(self, uuid: UUID) -> Recording:
        """Get recording by recording UUID.

        Args:
            uuid: Recording UUID

        Returns:
            Recording details including download URLs
        """
        data = await self.client._request("GET", f"/recordings/{uuid}")
        return Recording.model_validate(data)
