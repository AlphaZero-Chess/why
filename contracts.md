# Virtual Chromium Browser - API Contracts

## Overview
Full-stack virtual browser with Playwright-based headless Chromium, real-time streaming, and extensions support.

## API Endpoints

### Browser Session Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/browser/session` | Create new browser session |
| DELETE | `/api/browser/session/{session_id}` | Close browser session |
| GET | `/api/browser/session/{session_id}/status` | Get session status |

### Navigation
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/browser/{session_id}/navigate` | Navigate to URL |
| POST | `/api/browser/{session_id}/back` | Go back |
| POST | `/api/browser/{session_id}/forward` | Go forward |
| POST | `/api/browser/{session_id}/refresh` | Refresh page |
| GET | `/api/browser/{session_id}/screenshot` | Get current screenshot |

### Input Events
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/browser/{session_id}/click` | Mouse click at position |
| POST | `/api/browser/{session_id}/type` | Type text |
| POST | `/api/browser/{session_id}/keypress` | Send key event |
| POST | `/api/browser/{session_id}/scroll` | Scroll page |

### Extensions
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/extensions` | List all extensions |
| POST | `/api/extensions/load` | Load unpacked extension |
| POST | `/api/extensions/pack` | Pack extension to .crx |
| PUT | `/api/extensions/{ext_id}/toggle` | Enable/disable extension |
| DELETE | `/api/extensions/{ext_id}` | Remove extension |

### Search & AI
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/search/suggestions` | Get AI-powered search suggestions |

## WebSocket
| Endpoint | Description |
|----------|-------------|
| `/api/ws/browser/{session_id}` | Real-time screenshot streaming & input |

## Mock Data to Replace
- `mockTabs` → Session-based tab management
- `mockExtensions` → MongoDB extensions collection
- `mockSearchSuggestions` → AI-generated via Emergent LLM
- `screenshot` state → Real Playwright screenshots

## Frontend Integration Points
1. `BrowserViewport.jsx` - Connect to WebSocket for streaming
2. `AddressBar.jsx` - Call `/api/search/suggestions` for AI suggestions
3. `VirtualBrowser.jsx` - Session management API calls
4. `ExtensionsPanel.jsx` - Extensions CRUD API calls

## Data Models

### BrowserSession
```json
{
  "session_id": "uuid",
  "created_at": "datetime",
  "current_url": "string",
  "title": "string",
  "can_go_back": "boolean",
  "can_go_forward": "boolean"
}
```

### Extension
```json
{
  "id": "string",
  "name": "string",
  "version": "string",
  "description": "string",
  "enabled": "boolean",
  "path": "string",
  "size": "string"
}
```
