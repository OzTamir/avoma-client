from typing import Any, Dict, Optional
import aiohttp
import logging
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
from .logging import create_logger, DEFAULT_FORMAT


class AvomaClient:
    """Base client for the Avoma API."""

    BASE_URL = "https://api.avoma.com/v1"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        session: Optional[aiohttp.ClientSession] = None,
        log_level: int = logging.INFO,
        logger_name: str = "avoma",
        log_format: Optional[str] = None,
    ):
        """Initialize the Avoma client.

        Args:
            api_key: The API key for authentication
            base_url: Optional custom base URL for the API
            session: Optional aiohttp ClientSession to use
            log_level: Logging level (default: INFO)
            logger_name: Name for the logger (default: "avoma")
            log_format: Optional custom log format string
        """
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL
        self._session = session

        # Configure logging
        self.logger = create_logger(
            name=logger_name,
            level=log_level,
            format_string=log_format or DEFAULT_FORMAT,
        )
        self.logger.debug(f"Initializing Avoma client with base URL: {self.base_url}")

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
        self.logger.debug("Entering context manager")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.logger.debug("Exiting context manager")
        await self.close()

    @property
    def session(self) -> aiohttp.ClientSession:
        """Get or create the aiohttp ClientSession."""
        if self._session is None:
            self.logger.debug("Creating new aiohttp ClientSession")
            self._session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
        return self._session

    async def close(self):
        """Close the client session."""
        if self._session is not None:
            self.logger.debug("Closing aiohttp ClientSession")
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
        url = f"{self.base_url}/{path.lstrip('/')}/"

        # Log request details
        request_id = id(params) + id(json) if params or json else id(url)
        self.logger.debug(f"Request {request_id}: {method} {url}")
        if params:
            self.logger.debug(f"Request {request_id} params: {params}")
        if json:
            self.logger.debug(f"Request {request_id} body: {json}")

        async with self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
        ) as response:
            json_response = await response.json()

            # Log response details
            status = response.status
            self.logger.debug(f"Response {request_id}: status={status}")
            if status >= 400:
                self.logger.error(f"Error response {request_id}: {json_response}")
            elif self.logger.isEnabledFor(logging.DEBUG):
                # Only log full response body at DEBUG level
                self.logger.debug(f"Response {request_id} body: {json_response}")

            response.raise_for_status()
            return json_response
