/**
 * LocalAI Assistant - API Client
 * HTTP client for communicating with FastAPI backend
 * Author: Lucas Andre S
 */

import axios from 'axios'
import type { Conversation, Message } from './store'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Types
export interface CreateConversationRequest {
  title: string
  model: string
  temperature: number
  top_p: number
  top_k: number
  max_tokens: number
}

export interface SendMessageRequest {
  conversation_id?: string
  message: string
  model: string
  temperature: number
  top_p: number
  top_k: number
  max_tokens: number
}

export interface SendMessageResponse {
  conversation_id: string
  message: Message
}

export interface ModelsResponse {
  models: { name: string }[]
}

export interface SystemPrompt {
  id: string
  name: string
  description: string
  content: string
  category: string
  is_default?: boolean
}

export interface DashboardStats {
  total_conversations: number
  total_messages: number
  total_tokens: number
  average_response_time: number
  models_used: Record<string, number>
  conversations_today?: number
  messages_today?: number
  tokens_today?: number
  active_model?: string
  avg_response_time?: number
}

// API Endpoints
export const getConversations = async (): Promise<Conversation[]> => {
  try {
    const response = await apiClient.get<{ conversations: Conversation[] }>('/conversations/')
    const conversations = response.data.conversations || []
    console.log('✅ Fetched conversations:', conversations.length, conversations)
    return conversations
  } catch (error) {
    console.error('❌ Error fetching conversations:', error)
    return []
  }
}

export const getConversation = async (uuid: string): Promise<Conversation | null> => {
  try {
    const response = await apiClient.get<Conversation>(`/conversations/${uuid}`)
    return response.data
  } catch (error) {
    console.error('Error fetching conversation:', error)
    return null
  }
}

export const createConversation = async (
  data: CreateConversationRequest
): Promise<Conversation> => {
  try {
    const response = await apiClient.post<Conversation>('/conversations/', data)
    return response.data
  } catch (error) {
    console.error('Error creating conversation:', error)
    throw error
  }
}

export const deleteConversation = async (uuid: string): Promise<void> => {
  try {
    await apiClient.delete(`/conversations/${uuid}`)
  } catch (error) {
    console.error('Error deleting conversation:', error)
    throw error
  }
}

export const sendMessage = async (
  data: SendMessageRequest
): Promise<SendMessageResponse> => {
  try {
    const response = await apiClient.post<SendMessageResponse>('/chat/completions', data)
    return response.data
  } catch (error) {
    console.error('Error sending message:', error)
    throw error
  }
}

export let abortController: AbortController | null = null

export const sendMessageStream = async (
  data: SendMessageRequest,
  onChunk: (chunk: string, done: boolean) => void
): Promise<string> => {
  try {
    abortController = new AbortController()
    const response = await fetch(`${API_BASE_URL}/chat/completions/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
      signal: abortController.signal,
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body?.getReader()
    const decoder = new TextDecoder()
    let conversationId = ''
    let isDone = false

    if (!reader) {
      throw new Error('Response body is not readable')
    }

    while (true) {
      const { done, value } = await reader.read()

      if (done) {
        // Only call onChunk with done=true if we haven't already
        if (!isDone) {
          onChunk('', true)
        }
        break
      }

      const chunk = decoder.decode(value, { stream: true })
      const lines = chunk.split('\n')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const parsedData = JSON.parse(line.slice(6))
            if (parsedData.conversation_id) {
              conversationId = parsedData.conversation_id
            }
            // Only send content chunks if they have content
            if (parsedData.content && parsedData.content.trim()) {
              onChunk(parsedData.content, false)
            }
            // Mark as done when we receive the done signal
            if (parsedData.done && !parsedData.content) {
              isDone = true
              onChunk('', true)
            }
          } catch (e) {
            // Ignore parse errors
          }
        }
      }
    }

    return conversationId
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') {
      console.log('Stream aborted by user')
    } else {
      console.error('Error in stream:', error)
    }
    throw error
  } finally {
    abortController = null
  }
}

export const stopMessageStream = async (conversationId?: string) => {
  if (abortController) {
    abortController.abort()
    abortController = null
  }
  
  // Notify backend that generation was stopped
  try {
    const params = conversationId ? `?conversation_id=${conversationId}` : ''
    await apiClient.post(`/chat/stop-generation${params}`)
    console.log('✅ Stop signal sent to backend for conversation:', conversationId)
  } catch (error) {
    console.error('Error notifying backend of stop:', error)
  }
}

export const getModels = async (): Promise<ModelsResponse> => {
  try {
    const response = await apiClient.get<ModelsResponse>('/models/')
    return response.data
  } catch (error) {
    console.error('Error fetching models:', error)
    return { models: [{ name: 'dolphin-mistral' }] }
  }
}

export const getSystemPrompts = async (): Promise<SystemPrompt[]> => {
  try {
    const response = await apiClient.get<{ prompts: SystemPrompt[] }>('/prompts/')
    return response.data.prompts || []
  } catch (error) {
    console.error('Error fetching system prompts:', error)
    return []
  }
}

export const getDashboardStats = async (): Promise<DashboardStats> => {
  try {
    const response = await apiClient.get<DashboardStats>('/conversations/stats')
    return response.data
  } catch (error) {
    console.error('Error fetching dashboard stats:', error)
    return {
      total_conversations: 0,
      total_messages: 0,
      total_tokens: 0,
      average_response_time: 0,
      models_used: {},
      conversations_today: 0,
      messages_today: 0,
      tokens_today: 0,
      active_model: 'dolphin-mistral',
    }
  }
}

export default apiClient
