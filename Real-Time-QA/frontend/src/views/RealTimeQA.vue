<template>
  <div class="realtime-qa-container">
    <a-card class="qa-card" :bordered="false">
      <div class="chat-messages" ref="messageContainer">
        <div class="ai-welcome" v-if="messages.length === 0">
          <div class="ai-avatar">
            <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%231890ff'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 2c3.68 0 6.78 2.51 7.71 5.9-.6-.16-1.23-.27-1.88-.27-2.31 0-4.39.99-5.83 2.58-1.44-1.59-3.52-2.58-5.83-2.58-.65 0-1.28.11-1.88.27C5.22 6.51 8.32 4 12 4zm0 16c-3.87 0-7.14-2.67-8-6.35.5.07 1 .11 1.5.11 2.97 0 5.5-1.42 7.07-3.58l.43-.57.43.57c1.57 2.16 4.1 3.58 7.07 3.58.5 0 1-.04 1.5-.11-.86 3.68-4.13 6.35-8 6.35z'/%3E%3C/svg%3E" alt="AI Avatar" />
          </div>
          <h2>{{ t('realtimeQA.title') }}</h2>
          <p>{{ t('realtimeQA.startTip') }}</p>
        </div>
        <div v-for="(message, index) in messages" :key="index" 
             :class="['message', message.role === 'user' ? 'user-message' : 'ai-message']">
          <div class="message-avatar"></div>
          <div class="message-content">
            <div class="message-text">{{ message.content }}</div>
            <div class="message-time">{{ message.time }}</div>
          </div>
        </div>
      </div>

      <div class="control-panel">
        <div class="call-wrapper">
          <!-- No call status -->
          <div v-if="!isInCall" class="start-call-container">
            <div class="welcome-content">
              <div class="welcome-avatar">
                <div class="avatar-circle">
                  <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%231890ff'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 2c3.68 0 6.78 2.51 7.71 5.9-.6-.16-1.23-.27-1.88-.27-2.31 0-4.39.99-5.83 2.58-1.44-1.59-3.52-2.58-5.83-2.58-.65 0-1.28.11-1.88.27C5.22 6.51 8.32 4 12 4zm0 16c-3.87 0-7.14-2.67-8-6.35.5.07 1 .11 1.5.11 2.97 0 5.5-1.42 7.07-3.58l.43-.57.43.57c1.57 2.16 4.1 3.58 7.07 3.58.5 0 1-.04 1.5-.11-.86 3.68-4.13 6.35-8 6.35z'/%3E%3C/svg%3E" alt="AI Avatar" />
                </div>
                <div class="pulse-ring"></div>
              </div>
              <h2 class="welcome-title">{{ t('realtimeQA.welcomeTitle') }}</h2>
              <p class="welcome-subtitle">{{ t('realtimeQA.welcomeSubtitle') }}</p>
              <a-button 
                type="primary" 
                shape="circle" 
                class="call-btn-large"
                :loading="isConnecting"
                @click="startCall"
              >
                <template #icon><phone-outlined /></template>
              </a-button>
            </div>
          </div>

          <!-- In-call status -->
          <div v-else class="active-call-container">
            <div class="call-duration">{{ formatDuration }}</div>
            <div class="active-call-controls">
              <a-button 
                type="primary" 
                shape="circle" 
                class="mute-btn"
                :class="{ 'muted': isMuted }"
                @click="toggleMute"
              >
                <template #icon>
                  <audio-muted-outlined v-if="isMuted" />
                  <audio-outlined v-else />
                </template>
              </a-button>
              
              <a-dropdown>
                <a-button type="primary" shape="circle" class="voice-select-btn">
                  <template #icon><sound-outlined /></template>
                </a-button>
                <template #overlay>
                  <a-menu>
                    <a-menu-item v-for="voice in getAvailableVoices()" 
                                 :key="voice.name"
                                 @click="changeVoice(voice)">
                      {{ voice.name }}
                    </a-menu-item>
                  </a-menu>
                </template>
              </a-dropdown>

              <a-dropdown>
                <a-button type="primary" shape="circle" class="rate-select-btn">
                  <template #icon><thunderbolt-outlined /></template>
                </a-button>
                <template #overlay>
                  <a-menu>
                    <a-menu-item @click="changeSpeechRate(0.5)">0.5x</a-menu-item>
                    <a-menu-item @click="changeSpeechRate(0.75)">0.75x</a-menu-item>
                    <a-menu-item @click="changeSpeechRate(1.0)">1.0x</a-menu-item>
                    <a-menu-item @click="changeSpeechRate(1.25)">1.25x</a-menu-item>
                    <a-menu-item @click="changeSpeechRate(1.5)">1.5x</a-menu-item>
                    <a-menu-item @click="changeSpeechRate(2.0)">2.0x</a-menu-item>
                  </a-menu>
                </template>
              </a-dropdown>
              
              <a-button 
                type="primary" 
                danger
                shape="circle" 
                class="end-call-btn"
                @click="endCall(true)"
              >
                <template #icon><phone-outlined /></template>
              </a-button>
            </div>
          </div>
        </div>
      </div>
    </a-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { 
  AudioOutlined, 
  AudioMutedOutlined, 
  PhoneOutlined,
  SoundOutlined,
  ThunderboltOutlined
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { Disconnect } from '@/utils/api/RealTimeoa'
import { WebSocketHeartbeat } from '@/utils/WebSocketHeartbeat'

const { t } = useI18n()

const messages = ref([])
const messageContainer = ref(null)
const isConnected = ref(false)
const isInCall = ref(false)
const isConnecting = ref(false)
const isMuted = ref(false)
const isUserInitiated = ref(false)
const callStartTime = ref(null)
const currentTime = ref(Date.now())
const ws = ref(null)
const peerConnection = ref(null)
const localStream = ref(null)
const remoteStream = ref(null)
const connectionStatus = ref('Unconnected')
const clientId = ref(null) // Client ID
const isAIResponding = ref(false) // Whether AI is responding
const speechTimeout = ref(null) // Speech timeout timer
const lastSpeechTime = ref(Date.now()) // Last speech time
const synthesis = ref(null) // Speech synthesis instance
const heartbeatTimer = ref(null) // Heartbeat timer
const isSpeaking = ref(false) // Whether user is speaking
const selectedVoice = ref(null) // Selected voice for synthesis
const speechRate = ref(1.25) // Speech rate, default 1.0

// Speech recognition related
const recognition = ref(null)
const isListening = ref(false)
const interimTranscript = ref('')
const finalTranscript = ref('')

// Calculate call duration
const formatDuration = computed(() => {
  if (!callStartTime.value || !isInCall.value) return '00:00'
  const duration = Math.floor((currentTime.value - callStartTime.value) / 1000)
  const minutes = Math.floor(duration / 60).toString().padStart(2, '0')
  const seconds = (duration % 60).toString().padStart(2, '0')
  return `${minutes}:${seconds}`
})

// Update call duration
const updateCallDuration = () => {
  if (isInCall.value) {
    currentTime.value = Date.now()
    requestAnimationFrame(updateCallDuration)
  }
}

// Reset speech timer
const resetSpeechTimer = () => {
  if (speechTimeout.value) {
    clearTimeout(speechTimeout.value)
  }
  lastSpeechTime.value = Date.now()
  isSpeaking.value = true
  
  // Clear heartbeat timer
  if (heartbeatTimer.value) {
    clearTimeout(heartbeatTimer.value)
    heartbeatTimer.value = null
  }
  
  speechTimeout.value = setTimeout(() => {
    if (finalTranscript.value) {
      const speechMessage = {
        content: finalTranscript.value,
        timestamp: Date.now()
      }
      console.log('Send speech recognition result to backend:', speechMessage)
      sendMessage('chat', speechMessage)
      addMessage('user', finalTranscript.value)
      isAIResponding.value = true
      addMessage('system', 'realtimeQA.aiResponding', true)
      finalTranscript.value = '' // Clear current recognition result
      
      // Start heartbeat after user stops speaking for 10 seconds
      isSpeaking.value = false
      heartbeatTimer.value = setTimeout(() => {
        if (ws.value) {
          console.log('User stopped speaking for 10 seconds, start heartbeat')
          ws.value.startHeartbeat()
        }
      }, 10000)
    }
  }, 3000) // Send after 3 seconds
}

// Initialize speech synthesis
const initSpeechSynthesis = () => {
  if ('speechSynthesis' in window) {
    synthesis.value = window.speechSynthesis
    // Wait for voice list to load
    const loadVoices = () => {
      const voices = synthesis.value.getVoices()
      // Filter Chinese voices
      const chineseVoices = voices.filter(voice => voice.lang.includes('zh'))
      if (chineseVoices.length > 0) {
        // Select first Chinese voice by default
        selectedVoice.value = chineseVoices[0]
      }
    }
    
    // If voice list is already loaded
    if (synthesis.value.getVoices().length > 0) {
      loadVoices()
    } else {
      // Wait for voice list to load
      synthesis.value.onvoiceschanged = loadVoices
    }
  } else {
    message.error(t('realtimeQA.speechSynthesisError'))
  }
}

// Convert text to speech and play
const speakText = (text) => {
  if (!synthesis.value) return
  
  // Stop currently playing speech
  synthesis.value.cancel()
  
  // Create new speech synthesis request
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = 'zh-CN'
  utterance.rate = speechRate.value // Use current speech rate
  utterance.pitch = 1.0
  utterance.volume = 1.0
  
  // Use selected voice
  if (selectedVoice.value) {
    utterance.voice = selectedVoice.value
  }
  
  // Play speech
  synthesis.value.speak(utterance)
}

// Change voice
const changeVoice = (voice) => {
  selectedVoice.value = voice
  message.success(t('realtimeQA.voiceChanged'))
}

// Get available Chinese voices
const getAvailableVoices = () => {
  if (!synthesis.value) return []
  return synthesis.value.getVoices().filter(voice => voice.lang.includes('zh'))
}

// Change speech rate
const changeSpeechRate = (rate) => {
  speechRate.value = rate
  message.success(t('realtimeQA.rateChanged', { rate }))
}

// Initialize WebSocket
const initSocket = () => {
  return new Promise((resolve, reject) => {
    try {
      ws.value = new WebSocketHeartbeat('ws://localhost:8000/ws/chat', {
        onopen: (event) => {
          console.log('WebSocket connection established')
          isConnected.value = true
          connectionStatus.value = t('realtimeQA.connected')
          message.success(t('realtimeQA.wsConnected'))
          resolve()
        },
        onmessage: async (event) => {
          try {
            const data = JSON.parse(event.data)
            console.log('Received WebSocket data:', data)
            switch (data.type) {
              case 'system':
                // Parse and save client ID
                if (data.content.includes('Client ID:')) {
                  clientId.value = data.content.split('Client ID:')[1].trim()
                }
                break
              case 'call-ended':
                endCall(false)
                break
              case 'chat':
                // Received AI response
                isAIResponding.value = false
                // Only show message and play speech if content exists
                if (data.content && data.content.trim()) {
                  addMessage('ai', data.content)
                  speakText(data.content)
                }
                break
            }
          } catch (err) {
            console.error('Failed to process message:', err)
          }
        },
        onclose: (event) => {
          console.log('WebSocket connection closed')
          isConnected.value = false
          connectionStatus.value = t('realtimeQA.disconnected')
          if (isInCall.value && !isUserInitiated.value) {
            message.error(t('realtimeQA.wsDisconnected'))
          }
          // if (isInCall.value) {
          //   endCall(false)
          // }
          reject(event)
        },
        onerror: (error) => {
          console.error('WebSocket connection error:', error)
          isConnected.value = false
          connectionStatus.value = t('realtimeQA.connectionFailed')
          message.error(t('realtimeQA.wsError'))
          reject(error)
        }
      })
    } catch (err) {
      console.error('WebSocket initialization failed:', err)
      message.error(t('realtimeQA.initError'))
      reject(err)
    }
  })
}

// Helper function to send messages
const sendMessage = (type, data) => {
  return new Promise((resolve, reject) => {
    const trySendMessage = () => {
      if (ws.value && ws.value.ws && ws.value.ws.readyState === WebSocket.OPEN) {
        const message = { type, ...data }
        console.log('Message sent to backend:', message)
        ws.value.sendMessage(message)
        resolve()
      } else {
        console.log('WebSocket not connected, waiting for connection...')
        // Wait for connection to establish before sending message
        setTimeout(() => {
          if (ws.value && ws.value.ws && ws.value.ws.readyState === WebSocket.OPEN) {
            const message = { type, ...data }
            console.log('Connection established, sending message:', message)
            ws.value.sendMessage(message)
            resolve()
          } else {
            console.error('WebSocket connection failed, cannot send message')
            reject(new Error('WebSocket connection failed, cannot send message'))
          }
        }, 2000) // Increase wait time to 2 seconds
      }
    }
    trySendMessage()
  })
}

// Initialize WebRTC
const initWebRTC = () => {
  peerConnection.value = new RTCPeerConnection({
    iceServers: [
      { urls: 'stun:stun.l.google.com:19302' }
    ]
  })

  // Handle ICE candidates
  peerConnection.value.onicecandidate = (event) => {
    if (event.candidate) {
      // Wrap sendMessage call in Promise
      sendMessage('ice-candidate', { candidate: event.candidate })
        .catch(err => console.error('Failed to send ICE candidate:', err))
    }
  }

  // Handle remote stream
  peerConnection.value.ontrack = (event) => {
    remoteStream.value = event.streams[0]
    const audioElement = new Audio()
    audioElement.srcObject = remoteStream.value
    audioElement.play()
  }
}

// Initialize speech recognition
const initSpeechRecognition = () => {
  if ('webkitSpeechRecognition' in window) {
    recognition.value = new webkitSpeechRecognition()
    recognition.value.continuous = true
    recognition.value.interimResults = true
    recognition.value.lang = 'zh-CN'

    recognition.value.onresult = (event) => {
      interimTranscript.value = ''
      finalTranscript.value = ''

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript
        if (event.results[i].isFinal) {
          finalTranscript.value += transcript
        } else {
          interimTranscript.value += transcript
        }
      }

      // Reset timer if there is a final result
      if (finalTranscript.value) {
        resetSpeechTimer()
      }
    }

    recognition.value.onerror = (event) => {
      // Only show error message for specific error types
      if (event.error === 'no-speech') {
        // Don't show error when no speech is detected
        return
      }
      console.warn('Speech recognition error:', event.error)
      message.error(t('realtimeQA.speechRecognitionError'))
    }

    recognition.value.onend = () => {
      if (isInCall.value && !isMuted.value) {
        // Add small delay before restarting recognition
        setTimeout(() => {
          if (isInCall.value && !isMuted.value) {
            recognition.value.start()
          }
        }, 100)
      }
    }
  } else {
    message.error(t('realtimeQA.speechRecognitionError'))
  }
}

// Start speech recognition
const startListening = () => {
  if (recognition.value && !isListening.value) {
    recognition.value.start()
    isListening.value = true
    addMessage('system', 'realtimeQA.recognitionStarted', true)
  }
}

// Stop speech recognition
const stopListening = () => {
  if (recognition.value && isListening.value) {
    recognition.value.stop()
    isListening.value = false
    addMessage('system', 'realtimeQA.recognitionStopped', true)
  }
}

// Start call
const startCall = async () => {
  try {
    isConnecting.value = true
    
    // First get microphone permission
    try {
      localStream.value = await navigator.mediaDevices.getUserMedia({ 
        audio: true,
        video: false
      })
      console.log('Successfully obtained microphone permission')
    } catch (err) {
      console.error('Failed to get microphone permission:', err)
      message.error(t('realtimeQA.micPermissionError'))
      return
    }
    
    // Then initialize WebSocket connection
    await initSocket()
    
    // Finally initialize WebRTC
    await initWebRTC()
    
    // Add audio tracks to connection
    localStream.value.getTracks().forEach(track => {
      peerConnection.value.addTrack(track, localStream.value)
    })

    const offer = await peerConnection.value.createOffer()
    await peerConnection.value.setLocalDescription(offer)
    await sendMessage('offer', { offer })

    isInCall.value = true
    callStartTime.value = Date.now()
    updateCallDuration()
    addMessage('system', 'realtimeQA.callStarted', true)
    
    // Start speech recognition
    if (!isMuted.value) {
      startListening()
    }
  } catch (err) {
    console.error('Failed to start call:', err)
    message.error(t('realtimeQA.startCallError'))
    // Clean up resources on error
    if (localStream.value) {
      localStream.value.getTracks().forEach(track => track.stop())
    }
    if (ws.value) {
      ws.value.close()
    }
    isInCall.value = false
    isConnecting.value = false
  } finally {
    isConnecting.value = false
  }
}

// End call
const endCall = async (isUserInitiatedParam = false) => {
  isUserInitiated.value = isUserInitiatedParam
  if (localStream.value) {
    localStream.value.getTracks().forEach(track => track.stop())
  }
  if (peerConnection.value) {
    peerConnection.value.close()
  }
  
  // Stop speech recognition
  stopListening()
  
  // Stop speech synthesis
  if (synthesis.value) {
    synthesis.value.cancel()
  }
  
  // Clear speech timer
  if (speechTimeout.value) {
    clearTimeout(speechTimeout.value)
    speechTimeout.value = null
  }
  
  // Only call disconnect API if user initiated and has client ID
  if (isUserInitiated && isInCall.value && clientId.value) {
    try {
      let res = await Disconnect(clientId.value)
      console.log(res)
    } catch (error) {
      console.error('Failed to call disconnect API:', error)
    }
  }
  
  if (ws.value) {
    ws.value.close()
  }
  
  isInCall.value = false
  callStartTime.value = null
  localStream.value = null
  remoteStream.value = null
  clientId.value = null  // Reset client ID
  isAIResponding.value = false // Reset AI response status
}

// Toggle mute
const toggleMute = () => {
  isMuted.value = !isMuted.value
  if (isMuted.value) {
    stopListening()
  } else if (isInCall.value) {
    startListening()
  }
  addMessage('system', isMuted.value ? 'realtimeQA.muted' : 'realtimeQA.unmuted', true)
}

// Add message to list
const addMessage = (role, content, isSystemMessage = false) => {
  messages.value.push({
    role,
    content: isSystemMessage ? t(content) : content,
    time: new Date().toLocaleTimeString(),
    isSystemMessage
  })
  scrollToBottom()
}

// Watch language changes, update system messages
watch(() => t('realtimeQA.systemReady'), (newValue) => {
  messages.value = messages.value.map(msg => {
    if (msg.isSystemMessage) {
      return {
        ...msg,
        content: t(msg.content)
      }
    }
    return msg
  })
})

// Scroll to bottom
const scrollToBottom = async () => {
  await nextTick()
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
}

onMounted(() => {
  addMessage('system', 'realtimeQA.systemReady', true)
  initSpeechRecognition()
  initSpeechSynthesis()
})

onUnmounted(() => {
  if (recognition.value) {
    recognition.value.stop()
  }
  if (synthesis.value) {
    synthesis.value.cancel()
  }
})
</script>

<style scoped>
.realtime-qa-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: none;
  height: 100%;
  position: relative;
}

.qa-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: none;
  backdrop-filter: blur(10px);
  border-radius: 1rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  padding: 2rem 3rem 2rem 2rem;
  height: 100%;
  position: relative;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  margin-bottom: 0.5rem;
  background: none;
  border-radius: 0.5rem;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 180px;
  padding-bottom: 2rem;
  mask-image: linear-gradient(to bottom, transparent 0%, black 5%, black 95%, transparent 100%);
  -webkit-mask-image: linear-gradient(to bottom, transparent 0%, black 5%, black 95%, transparent 100%);
}

.message {
  margin-bottom: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.message-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background-size: cover;
  background-position: center;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 2px solid white;
}

.user-message {
  flex-direction: row-reverse;
}

.user-message .message-avatar {
  background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%231890ff"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/></svg>');
  background-color: #e6f7ff;
}

.ai-message .message-avatar {
  background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%231890ff"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 2c3.68 0 6.78 2.51 7.71 5.9-.6-.16-1.23-.27-1.88-.27-2.31 0-4.39.99-5.83 2.58-1.44-1.59-3.52-2.58-5.83-2.58-.65 0-1.28.11-1.88.27C5.22 6.51 8.32 4 12 4zm0 16c-3.87 0-7.14-2.67-8-6.35.5.07 1 .11 1.5.11 2.97 0 5.5-1.42 7.07-3.58l.43-.57.43.57c1.57 2.16 4.1 3.58 7.07 3.58.5 0 1-.04 1.5-.11-.86 3.68-4.13 6.35-8 6.35z"/></svg>');
  background-color: #f0f5ff;
}

.message-content {
  max-width: 80%;
  padding: 0.8rem 1.2rem;
  border-radius: 1rem;
  position: relative;
}

.user-message .message-content {
  background-color: #1890ff;
  color: white;
  border-top-right-radius: 0.2rem;
}

.ai-message .message-content {
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-top-left-radius: 0.2rem;
}

.message-time {
  font-size: 0.8rem;
  color: #999;
  margin-top: 0.4rem;
}

.control-panel {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  background: transparent;
  padding-bottom: 2rem;
  z-index: 10;
}

.call-wrapper {
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(10px);
}

.call-container {
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
}

.connection-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.voice-controls {
  display: flex;
  justify-content: center;
  padding: 1.5rem 0 0.5rem;
}

.call-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.ai-call-avatar {
  width: 80px;
  height: 80px;
  border-radius: 40px;
  background: #f0f5ff;
  padding: 16px;
  margin-bottom: 1rem;
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.15);
  animation: pulse 2s infinite;
}

.ai-call-avatar img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.active-call-controls {
  display: flex;
  align-items: center;
  gap: 3rem;
  padding: 1rem 2rem;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 3rem;
}

.call-btn {
  width: 5rem;
  height: 5rem;
  font-size: 2rem;
  background: #52c41a;
  border-color: #52c41a;
  box-shadow: 0 4px 12px rgba(82, 196, 26, 0.3);
}

.call-btn:hover {
  background: #73d13d;
  border-color: #73d13d;
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(82, 196, 26, 0.4);
}

.mute-btn, .end-call-btn {
  width: 4rem;
  height: 4rem;
  font-size: 1.5rem;
}

.mute-btn {
  background: #1890ff;
  border-color: #1890ff;
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.2);
}

.mute-btn.muted {
  background: #ff4d4f;
  border-color: #ff4d4f;
  box-shadow: 0 4px 12px rgba(255, 77, 79, 0.2);
}

.end-call-btn {
  transform: rotate(135deg);
  box-shadow: 0 4px 12px rgba(255, 77, 79, 0.2);
}

.end-call-btn:hover {
  transform: rotate(135deg) scale(1.05);
  box-shadow: 0 6px 16px rgba(255, 77, 79, 0.3);
}

.voice-tip {
  font-size: 1rem;
  color: #8c8c8c;
  margin-top: 0.5rem;
}

.status-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ff4d4f;
  transition: all 0.3s;
}

.status-indicator.active {
  background-color: #52c41a;
}

.call-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.call-status {
  font-size: 0.9rem;
  color: #1890ff;
  font-weight: 500;
}

.call-duration {
  font-size: 1rem;
  color: #1890ff;
  font-weight: 500;
  font-family: monospace;
}

.ai-welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #8c8c8c;
  text-align: center;
  padding: 2rem;
}

.ai-welcome h2 {
  margin: 1rem 0 0.5rem;
  color: #1890ff;
  font-weight: 500;
}

.ai-welcome p {
  margin: 0;
  font-size: 0.9rem;
}

.ai-avatar {
  width: 120px;
  height: 120px;
  border-radius: 60px;
  background: #f0f5ff;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.15);
}

.ai-avatar img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* Custom scrollbar styles */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: transparent;
}

.chat-messages::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.2);
}

:deep(.ant-card) {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: rgba(255, 255, 255, 0.4);
}

:deep(.ant-card-body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0;
  overflow: hidden;
}

.start-call-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: 23rem;
}

.welcome-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  animation: fadeIn 0.5s ease-out;
  width: 100%;
}

.welcome-avatar {
  position: relative;
  width: 10rem;
  height: 10rem;
  margin-bottom: 2rem;
}

.avatar-circle {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: #f0f5ff;
  padding: 32px;
  box-shadow: 0 8px 24px rgba(24, 144, 255, 0.2);
  position: relative;
  z-index: 1;
  animation: float 3s ease-in-out infinite;
}

.avatar-circle img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.pulse-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid #1890ff;
  animation: pulse 2s ease-out infinite;
}

.welcome-title {
  font-size: 2rem;
  color: #1890ff;
  margin-bottom: 1rem;
  font-weight: 600;
  background: linear-gradient(45deg, #1890ff, #722ed1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.welcome-subtitle {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 2rem;
  max-width: 400px;
  line-height: 1.6;
}

.call-btn-large {
  width: 6rem;
  height: 6rem;
  font-size: 2.5rem;
  background: linear-gradient(45deg, #52c41a, #1890ff);
  border: none;
  box-shadow: 0 8px 24px rgba(82, 196, 26, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  animation: bounce 2s ease-in-out infinite;
}

.call-btn-large:hover {
  transform: scale(1.1);
  box-shadow: 0 12px 32px rgba(82, 196, 26, 0.4);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes pulse {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.2);
    opacity: 0;
  }
}

@keyframes bounce {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.active-call-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  gap: 1rem;
}

.call-duration {
  font-size: 1.2rem;
  color: #1890ff;
  font-weight: 500;
  font-family: monospace;
  margin-bottom: 0.5rem;
}

.voice-select-btn {
  background: #722ed1;
  border-color: #722ed1;
  box-shadow: 0 4px 12px rgba(114, 46, 209, 0.2);
}

.voice-select-btn:hover {
  background: #9254de;
  border-color: #9254de;
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(114, 46, 209, 0.3);
}

.rate-select-btn {
  background: #faad14;
  border-color: #faad14;
  box-shadow: 0 4px 12px rgba(250, 173, 20, 0.2);
}

.rate-select-btn:hover {
  background: #ffc53d;
  border-color: #ffc53d;
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(250, 173, 20, 0.3);
}
</style> 