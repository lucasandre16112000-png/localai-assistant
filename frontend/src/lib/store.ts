/**
 * LocalAI Assistant - Global State Management
 * Using Zustand for state management
 * Author: Lucas Andre S
 */

import { create } from 'zustand'

export interface Message {
  uuid?: string
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  generation_time?: number
  tokens?: number
}

export interface Conversation {
  uuid: string
  title: string
  model: string
  temperature: number
  top_p: number
  top_k: number
  max_tokens: number
  messages: Message[]
  created_at: string
  updated_at: string
  is_pinned?: boolean
  is_archived?: boolean
}

export interface Settings {
  defaultModel: string
  temperature: number
  topP: number
  topK: number
  maxTokens: number
  streamResponses: boolean
  theme: 'dark' | 'light'
  autoSave?: boolean
}

interface StoreState {
  // UI State
  sidebarOpen: boolean
  setSidebarOpen: (open: boolean) => void
  currentView: 'chat' | 'dashboard' | 'settings'
  setCurrentView: (view: 'chat' | 'dashboard' | 'settings') => void

  // Conversations
  conversations: Conversation[]
  setConversations: (conversations: Conversation[]) => void
  addConversation: (conversation: Conversation) => void
  removeConversation: (uuid: string) => void
  activeConversationId: string | null
  setActiveConversation: (uuid: string | null) => void

  // Chat State
  isGenerating: boolean
  setIsGenerating: (generating: boolean) => void
  streamingContent: string
  setStreamingContent: (content: string) => void
  appendStreamingContent: (content: string) => void

  // Models
  models: string[]
  setModels: (models: string[]) => void
  activeModel: string
  setActiveModel: (model: string) => void

  // Settings
  settings: Settings
  updateSettings: (settings: Partial<Settings>) => void
}

const defaultSettings: Settings = {
  defaultModel: 'dolphin-mistral',
  temperature: 0.7,
  topP: 0.9,
  topK: 40,
  maxTokens: 2048,
  streamResponses: true,
  theme: 'dark',
  autoSave: true,
}

export const useStore = create<StoreState>((set) => ({
  // UI State
  sidebarOpen: true,
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  currentView: 'chat',
  setCurrentView: (view) => set({ currentView: view }),

  // Conversations
  conversations: [],
  setConversations: (conversations) => set({ conversations }),
  addConversation: (conversation) =>
    set((state) => ({
      conversations: [conversation, ...state.conversations],
    })),
  removeConversation: (uuid) =>
    set((state) => ({
      conversations: state.conversations.filter((c) => c.uuid !== uuid),
    })),
  activeConversationId: null,
  setActiveConversation: (uuid) => set({ activeConversationId: uuid }),

  // Chat State
  isGenerating: false,
  setIsGenerating: (generating) => set({ isGenerating: generating }),
  streamingContent: '',
  setStreamingContent: (content) => set({ streamingContent: content }),
  appendStreamingContent: (content) =>
    set((state) => ({
      streamingContent: state.streamingContent + content,
    })),

  // Models
  models: [],
  setModels: (models) => set({ models }),
  activeModel: 'dolphin-mistral',
  setActiveModel: (model) => set({ activeModel: model }),

  // Settings
  settings: defaultSettings,
  updateSettings: (newSettings) =>
    set((state) => ({
      settings: { ...state.settings, ...newSettings },
    })),
}))
