# Real-time Q&A module in Agentographer  (Frontend)

## Project Introduction

Agentographer is an AI medical assistant application developed with Vue 3, offering real-time voice Q&A, multilingual support, and other features. The application aims to assist medical diagnosis and consultation through artificial intelligence technology, providing a convenient interactive experience for medical professionals and patients.

## Technology Stack

- **Frontend Framework**: Vue 3
- **UI Component Libraries**: Element Plus, Ant Design Vue
- **Router Management**: Vue Router
- **Internationalization**: Vue I18n
- **Build Tool**: Vite
- **Network Communication**: Axios, Socket.io

## Features

- **Real-time Voice Q&A**: Support real-time voice conversations with AI assistants
- **Multilingual Support**: Support switching between Chinese and English
- **Responsive Design**: Adapt to different device screens
- **Voice Synthesis Control**: Adjustable speech rate and voice selection
- **WebSocket Communication**: Implement real-time data transmission

## Project Structure

```
├── public/             # Static resources
├── src/                # Source code
│   ├── assets/         # Asset files
│   ├── components/     # Components
│   ├── locales/        # Internationalization files
│   ├── router/         # Router configuration
│   ├── utils/          # Utility functions
│   ├── views/          # Page views
│   ├── App.vue         # Main application component
│   └── main.js         # Entry file
├── index.html          # HTML template
├── package.json        # Project dependencies
└── vite.config.js      # Vite configuration
```

## Installation and Running

### Requirements

- Node.js 16.0 or higher
- npm or yarn package manager

### Install Dependencies

```bash
# Using npm
npm install

# Or using yarn
yarn install
```

### Run in Development Mode

```bash
# Using npm
npm run dev

# Or using yarn
yarn dev
```

### Build for Production

```bash
# Using npm
npm run build

# Or using yarn
yarn build
```

### Preview Production Build

```bash
# Using npm
npm run preview

# Or using yarn
yarn preview
```

## Configuration

### API Server Configuration

To configure the backend API server for your application, modify the proxy settings in the `vite.config.js` file:

```js
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',  // Change to your backend server address
      changeOrigin: true,
      secure: false,
      rewrite: (path) => path.replace(/^\/api/, '/api')
    }
  }
}
```

With this configuration, all requests from the frontend application that start with `/api` will be proxied to the specified backend server.

### WebSocket Configuration

The application uses WebSockets for real-time communication. In the `RealTimeQA.vue` component, the WebSocket connection is configured as follows:

```js
ws.value = new WebSocketHeartbeat('ws://localhost:8000/ws/chat', {
  // WebSocket configuration options
  onopen: (event) => {
    // Callback when connection is established
  },
  onmessage: async (event) => {
    // Callback when message is received
  },
  // Other callbacks...
})
```

To modify the WebSocket server address, update the URL above. If you need to proxy WebSocket connections through Vite, add the following configuration to `vite.config.js`:

```js
server: {
  proxy: {
    // Existing API proxy configuration...
    
    '/ws': {
      target: 'ws://your-websocket-server.com',
      ws: true,  // Enable WebSocket proxy
      changeOrigin: true
    }
  }
}
```

After configuration, you can use relative paths (like `/ws/chat`) to connect to WebSockets in your code, and Vite will handle the proxying automatically.

### WebSocketHeartbeat Configuration Options

The `WebSocketHeartbeat` class supports the following configuration options:

- `pingInterval`: Heartbeat packet sending interval (milliseconds), default 30000
- `pingTimeout`: Heartbeat timeout (milliseconds), default 30000
- `reconnectInterval`: Reconnection interval (milliseconds), default 10000
- `maxReconnectAttempts`: Maximum reconnection attempts, default 20
- `onopen`: Callback function when connection is established
- `onmessage`: Callback function when message is received
- `onclose`: Callback function when connection is closed
- `onerror`: Callback function when connection error occurs

### Speech Synthesis Configuration

The application uses the Web Speech API for text-to-speech functionality. The speech synthesis is configured in the `RealTimeQA.vue` component:

```js
// Create new speech synthesis request
const utterance = new SpeechSynthesisUtterance(text)
utterance.lang = 'zh-CN'  // Set language
utterance.rate = speechRate.value  // Speech rate
utterance.pitch = 1.0  // Speech pitch
utterance.volume = 1.0  // Speech volume

// Use selected voice
if (selectedVoice.value) {
  utterance.voice = selectedVoice.value
}
```

You can modify these settings to customize the speech synthesis behavior according to your requirements.

## Main Functional Modules

### Real-time Voice Q&A

The real-time voice Q&A feature allows users to converse with AI assistants through voice. The system automatically recognizes user speech, converts it to text, and sends it to AI for processing. The AI's response is then converted to voice output through speech synthesis technology.

### Multilingual Support

The application supports both Chinese and English languages, and users can switch languages at any time. Internationalization is implemented based on Vue I18n, with all text content stored in language files for easy maintenance and expansion.

## Contribution Guidelines

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
