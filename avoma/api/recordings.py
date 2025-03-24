from uuid import UUID
from ..models.recordings import Recording


class RecordingsAPI:
    """API endpoints for recordings."""

    def __init__(self, client):
        self.client = client
        self.client.logger.debug("RecordingsAPI initialized")

    async def get_by_meeting(self, meeting_uuid: UUID) -> Recording:
        """Get recording by meeting UUID.

        Args:
            meeting_uuid: Meeting UUID

        Returns:
            Recording details including download URLs
        """
        self.client.logger.debug(f"Getting recording for meeting: {meeting_uuid}")
        data = await self.client._request(
            "GET", "/recordings", params={"meeting_uuid": str(meeting_uuid)}
        )
        recording = Recording.model_validate(data)
        self.client.logger.debug(f"Retrieved recording for meeting: {meeting_uuid}")
        return recording

    async def get(self, uuid: UUID) -> Recording:
        """Get recording by recording UUID.

        Args:
            uuid: Recording UUID

        Returns:
            Recording details including download URLs
        """
        self.client.logger.debug(f"Getting recording with UUID: {uuid}")
        data = await self.client._request("GET", f"/recordings/{uuid}")
        recording = Recording.model_validate(data)
        self.client.logger.debug(f"Retrieved recording: {uuid}")
        return recording
