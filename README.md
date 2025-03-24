# Avoma Python Client

An unofficial async Python client for the [Avoma API](https://api.avoma.com/docs).

## Installation

```bash
pip install avoma-client
```

Or with Poetry:

```bash
poetry add avoma-client
```

## Usage

```python
import asyncio
from avoma import AvomaClient
from datetime import datetime, timedelta

async def main():
    # Initialize the client with your API key
    client = AvomaClient("your-api-key")

    # Get meetings from the last 7 days
    now = datetime.utcnow()
    seven_days_ago = now - timedelta(days=7)

    meetings = await client.meetings.list(
        from_date=seven_days_ago.isoformat(),
        to_date=now.isoformat()
    )

    for meeting in meetings.results:
        print(f"Meeting: {meeting.subject} at {meeting.start_at}")

        # Get meeting insights if available
        if meeting.state == "completed":
            insights = await client.meetings.get_insights(meeting.uuid)
            print(f"Meeting insights: {insights}")

asyncio.run(main())
```

## Logging

The client includes built-in logging functionality. You can configure logging directly through the client:

```python
import logging
from avoma import AvomaClient

# Set log level directly in the client constructor
client = AvomaClient(
    api_key="your-api-key",
    log_level=logging.DEBUG,
    logger_name="my-app.avoma"  # Optional custom logger name
)
```

For more advanced logging configuration:

```python
import logging
import sys
from avoma import AvomaClient, create_logger

# Create a client with custom logging
client = AvomaClient("your-api-key", log_level=logging.DEBUG)

# Customize the logger with a specific handler if needed
handler = logging.FileHandler("avoma.log")
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))

# Replace default handler with custom one
for h in client.logger.handlers:
    client.logger.removeHandler(h)
client.logger.addHandler(handler)
```

The logs include:

- API request and response details (with sensitive data redacted)
- Client lifecycle events
- API call information

This is useful for debugging API interactions and understanding the client's behavior.

## Features

- Fully async API using aiohttp
- Type hints and Pydantic models for all responses
- Comprehensive test coverage
- Detailed logging for debugging
- Support for all Avoma API endpoints:
  - Meetings
  - Recordings
  - Transcriptions
  - Smart Categories
  - Templates
  - Notes
  - Meeting Sentiments
  - Users
  - Calls
  - Scorecards
  - Webhooks

## Development

1. Clone the repository
2. Install dependencies:

```bash
poetry install
```

3. Run tests:

```bash
poetry run pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License
