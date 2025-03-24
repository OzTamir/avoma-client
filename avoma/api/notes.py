from typing import Optional
from uuid import UUID

from ..models.notes import Note, NotesList, NotesQuery


class NotesAPI:
    """API endpoints for notes."""

    def __init__(self, client):
        self.client = client
        self.client.logger.debug("NotesAPI initialized")

    async def list(
        self,
        from_date: str,
        to_date: str,
        meeting_uuid: Optional[UUID] = None,
        custom_category: Optional[UUID] = None,
        output_format: str = "json",
        page_size: Optional[int] = None,
    ) -> NotesList:
        """List notes with optional filters.

        Args:
            from_date: Start date-time in ISO format
            to_date: End date-time in ISO format
            meeting_uuid: Optional meeting UUID to filter by
            custom_category: Optional custom category UUID to filter by
            output_format: Format of the notes (json, html, markdown)
            page_size: Number of notes per page (max 20)

        Returns:
            Paginated list of notes
        """
        self.client.logger.debug(f"Listing notes from {from_date} to {to_date}")

        if meeting_uuid:
            self.client.logger.debug(f"Filtering by meeting UUID: {meeting_uuid}")
        if custom_category:
            self.client.logger.debug(f"Filtering by custom category: {custom_category}")

        query = NotesQuery(
            from_date=from_date,
            to_date=to_date,
            meeting_uuid=meeting_uuid,
            custom_category=custom_category,
            output_format=output_format,
        )

        params = query.model_dump(exclude_none=True)
        # Convert UUID objects to strings
        if meeting_uuid:
            params["meeting_uuid"] = str(meeting_uuid)
        if custom_category:
            params["custom_category"] = str(custom_category)
        if page_size is not None:
            params["page_size"] = page_size

        data = await self.client._request("GET", "notes", params=params)
        notes_list = NotesList.model_validate(data)
        self.client.logger.debug(f"Retrieved {len(notes_list.results)} notes")
        return notes_list
