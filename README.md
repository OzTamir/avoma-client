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

## Features

- Fully async API using aiohttp
- Type hints and Pydantic models for all responses
- Comprehensive test coverage
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
