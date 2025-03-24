from typing import Any, Dict, Optional
import aiohttp
from yarl import URL

from .api.meetings import MeetingsAPI
from .api.recordings import RecordingsAPI
from .api.transcriptions import TranscriptionsAPI
from .api.smart_categories import SmartCategoriesAPI
from .api.templates import TemplatesAPI
from .api.notes import NotesAPI
from .api.sentiments import SentimentsAPI
from .api.users import UsersAPI
from .api.calls import CallsAPI


class AvomaClient:
    """Base client for the Avoma API."""

    BASE_URL = "https://api.avoma.com"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        """Initialize the Avoma client.

        Args:
            api_key: The API key for authentication
            base_url: Optional custom base URL for the API
            session: Optional HTTP session to use
        """
        self.api_key = api_key
        self.base_url = URL(base_url or self.BASE_URL)
        self._session = session

        # Initialize API endpoints
        self.meetings = MeetingsAPI(self)
        self.recordings = RecordingsAPI(self)
        self.transcriptions = TranscriptionsAPI(self)
        self.smart_categories = SmartCategoriesAPI(self)
        self.templates = TemplatesAPI(self)
        self.notes = NotesAPI(self)
        self.sentiments = SentimentsAPI(self)
        self.users = UsersAPI(self)
        self.calls = CallsAPI(self)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    @property
    def session(self) -> aiohttp.ClientSession:
        """Get or create the aiohttp ClientSession."""
        if self._session is None:
            self._session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
        return self._session

    async def close(self):
        """Close the client session."""
        if self._session is not None:
            await self._session.close()
            self._session = None

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a request to the Avoma API.

        Args:
            method: HTTP method
            path: API endpoint path
            params: Optional query parameters
            json: Optional JSON body

        Returns:
            API response as a dictionary

        Raises:
            aiohttp.ClientError: If the request fails
        """
        url = self.base_url.join(URL(path.lstrip("/")))

        async with self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
        ) as response:
            response.raise_for_status()
            return await response.json() if response.content_length else {}
