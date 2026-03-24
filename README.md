# CallPilot Voice Ops

A production-ready voice support platform that brings enterprise-grade call center capabilities to modern support teams. Built with FastAPI and designed for seamless integration with telephony providers like Twilio.

## Features

- **Intelligent Voice Orchestration**: Handles customer calls with intent recognition, sentiment analysis, and automatic escalation
- **Twilio Integration**: Ready-to-deploy webhook endpoints for live voice processing
- **Knowledge-Grounded Responses**: FAQ retrieval from indexed knowledge base with contextual answers
- **Real-Time Dashboard**: Live monitoring of active sessions, KPIs, and conversation timelines
- **Browser Simulator**: Test voice interactions without phone calls
- **Production Architecture**: Built for scalability with proper error handling and monitoring

## Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/iamarifalam/Voice-Agent.git
cd Voice-Agent
```

2. Install dependencies:
```bash
pip install -e .
```

3. Run the application:
```bash
uvicorn voice_agent_app.main:app --host 0.0.0.0 --port 8000
```

4. Open http://localhost:8000 in your browser

## Architecture

The system processes voice calls through several layers:

- **Telephony Layer**: Handles Twilio webhooks and TwiML responses
- **Orchestration Layer**: Manages conversation flow, intent classification, and escalation logic
- **Knowledge Layer**: Provides grounded responses from indexed FAQ content
- **Monitoring Layer**: Tracks sessions, metrics, and system health

## API Endpoints

### Voice Operations
- `GET /` - Main dashboard and simulator interface
- `POST /webhooks/twilio/voice` - Twilio voice webhook entry point
- `POST /webhooks/twilio/process` - Process voice transcripts

### Monitoring
- `GET /health` - System health check
- `GET /metrics` - Prometheus-compatible metrics
- `GET /dashboard` - Session and KPI data

### Simulator
- `POST /api/call/start` - Start a simulated call session
- `POST /api/transcript` - Process transcript and get agent response

## Deployment

### Docker
```bash
docker build -t voice-agent .
docker run -p 8000:8000 voice-agent
```

### Production Considerations
- Use a reverse proxy (nginx/Caddy) for SSL termination
- Configure environment variables for sensitive settings
- Set up proper logging and monitoring
- Use a production WSGI server like gunicorn

### Environment Variables
```bash
# Optional: Configure external services
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
ruff check src/ tests/
ruff format src/ tests/
```

## Integration Examples

### Twilio Setup
1. Create a Twilio phone number
2. Configure webhook URL: `https://yourdomain.com/webhooks/twilio/voice`
3. Set method to POST

### Custom Speech Providers
Replace the mock transcript processing with:
- Google Speech-to-Text
- Amazon Transcribe
- Deepgram

### CRM Integration
Extend the orchestrator to query:
- Order management systems
- Customer databases
- Ticket creation APIs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For questions or issues, please open a GitHub issue or contact the maintainers.

If you want this to look even closer to a large-company product, the next additions should be:

- Real caller authentication using order ID or CRM identity lookup
- Persistent storage for sessions and transcript history
- Queue assignment and agent handoff tracking
- Real-time streaming transcription
- Post-call QA scoring and cost tracking
- Role-based operator login for supervisors and support admins

## Resume Positioning

- Built a production-style voice support platform with telephony webhooks, intent routing, sentiment-aware escalation, and grounded FAQ retrieval.
- Designed an operator-facing support console with session KPIs, recent-call visibility, and conversation playback for demoable support workflows.
- Implemented a browser simulator and Twilio-compatible call flow to validate voice-support automation without paid voice infrastructure.
