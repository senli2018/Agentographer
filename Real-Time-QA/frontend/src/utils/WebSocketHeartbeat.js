export class WebSocketHeartbeat {
  constructor(url, options = {}) {

    this.url = url;
    this.pingInterval = options.pingInterval || 30000; 
    this.pingTimeout = options.pingTimeout || 30000;   
    this.reconnectInterval = options.reconnectInterval || 10000; 
    this.maxReconnectAttempts = options.maxReconnectAttempts || 20; 
    

    this.ws = null;
    this.pingTimeoutId = null;
    this.reconnectTimeoutId = null;
    this.reconnectAttempts = 0;
    this.forceClosed = false;
    

    this.onopen = options.onopen || (() => {});
    this.onmessage = options.onmessage || (() => {});
    this.onclose = options.onclose || (() => {});
    this.onerror = options.onerror || (() => {});
    

    this.connect();
  }
  
  // Establishing a connection
  connect() {
    if (this.ws) {
      this.ws.close();
    }
    
    this.forceClosed = false;
    this.ws = new WebSocket(this.url);
    

    this.ws.onopen = (event) => {

      this.reconnectAttempts = 0;
      this.startHeartbeat();
      
      // Send the first connection message
      this.sendMessage({
        type: 'ping',
        content: 'Initialize connection'
      });
      

      this.onopen(event);
    };
    
    // When a message is received
    this.ws.onmessage = (event) => {
      try {
        // If the message is empty, it returns
        if (!event.data) {
          return;
        }

        // Handling heartbeat responses
        const data = JSON.parse(event.data);
        if (data.type === 'ping' || data.type === 'pong') {
          this.resetPingTimeout();
        } else {

          this.onmessage(event);
        }
      } catch (err) {
        console.warn('Message parsing failed:', err);

        this.onmessage(event);
      }
    };
    
    // When the connection is closed
    this.ws.onclose = (event) => {

      this.stopHeartbeat();
      if (!this.forceClosed) {
        this.reconnect();
      }
      

      this.onclose(event);
    };
    
    // When an error occurs
    this.ws.onerror = (event) => {
      console.error('WebSocket connection error', event);
      

      this.onerror(event);
    };
  }
  
  // Start the heartbeat
  startHeartbeat() {
    this.stopHeartbeat();

    this.pingIntervalId = setInterval(() => {
      if (this.ws.readyState === WebSocket.OPEN) {
        // Sending heartbeat messages
        this.sendMessage({
          type: 'ping',
          content: 'ping',
          timestamp: Date.now()
        });
        
        // Set a heartbeat timeout
        this.pingTimeoutId = setTimeout(() => {
          console.warn('Heartbeat timeout, reconnect');
          this.ws.close();
        }, this.pingTimeout);
      }
    }, this.pingInterval);
  }
  
  // Stop heartbeat
  stopHeartbeat() {
    if (this.pingIntervalId) {
      clearInterval(this.pingIntervalId);
      this.pingIntervalId = null;
    }
    
    this.resetPingTimeout();
  }
  
  // Reset the heartbeat timeout
  resetPingTimeout() {
    if (this.pingTimeoutId) {
      clearTimeout(this.pingTimeoutId);
      this.pingTimeoutId = null;
    }
  }
  
  // Reconnect
  reconnect() {
    if (this.reconnectTimeoutId) {
      clearTimeout(this.reconnectTimeoutId);
    }
    
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Try reconnecting (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
      
      this.reconnectTimeoutId = setTimeout(() => {
        this.connect();
      }, this.reconnectInterval);
    } else {
      console.error(`The maximum number of reconnections is reached (${this.maxReconnectAttempts})Stop reconnecting`);
    }
  }
  
  // Sending messages
  sendMessage(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      console.warn('The WebSocket is not connected and cannot send messages');
    }
  }
  
  // Sending chat messages
  sendChatMessage(content) {
    this.sendMessage({
      type: 'chat',
      content: content
    });
  }
  
  // Actively close connections
  close() {
    this.forceClosed = true;
    this.stopHeartbeat();
    
    if (this.reconnectTimeoutId) {
      clearTimeout(this.reconnectTimeoutId);
      this.reconnectTimeoutId = null;
    }
    
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
} 