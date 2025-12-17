/**
 * LocalAI Assistant - Main App Component
 * Premium AI Assistant Application
 * Author: Lucas Andre S
 */

import React, { useEffect } from 'react'
import { AnimatePresence } from 'framer-motion'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Menu } from 'lucide-react'
import toast from 'react-hot-toast'

import { useStore, type Message } from './lib/store'
import {
  getConversations,
  getConversation,
  createConversation,
  deleteConversation,
  sendMessage,
  sendMessageStream,
  getModels,
} from './lib/api'

import { Sidebar } from './components/Sidebar/Sidebar'
import { Chat } from './components/Chat/Chat'
import { Dashboard } from './components/Dashboard/Dashboard'
import { Settings } from './components/Settings/Settings'

const App: React.FC = () => {
  const queryClient = useQueryClient()
  const {
    sidebarOpen,
    setSidebarOpen,
    currentView,
    setConversations,
    activeConversationId,
    setActiveConversation,
    addConversation,
    removeConversation,
    isGenerating,
    setIsGenerating,
    streamingContent,
    setStreamingContent,
    appendStreamingContent,
    setModels,
    settings,
  } = useStore()

  const { data: conversationsData } = useQuery({
    queryKey: ['conversations'],
    queryFn: getConversations,
    refetchInterval: 30000,
  })

  const { data: modelsData } = useQuery({
    queryKey: ['models'],
    queryFn: getModels,
  })

  const { data: activeConversation } = useQuery({
    queryKey: ['conversation', activeConversationId],
    queryFn: () => getConversation(activeConversationId!),
    enabled: !!activeConversationId,
  })

  useEffect(() => {
    if (conversationsData) {
      setConversations(conversationsData)
    }
  }, [conversationsData, setConversations])

  useEffect(() => {
    if (modelsData?.models) {
      const modelNames = modelsData.models.map((m: any) => typeof m === 'string' ? m : m.name)
      setModels(modelNames)
    }
  }, [modelsData, setModels])

  const createConversationMutation = useMutation({
    mutationFn: createConversation,
    onSuccess: (newConversation) => {
      addConversation(newConversation)
      setActiveConversation(newConversation.uuid)
      queryClient.invalidateQueries({ queryKey: ['conversations'] })
      toast.success('New conversation created')
    },
    onError: () => {
      toast.error('Failed to create conversation')
    },
  })

  const deleteConversationMutation = useMutation({
    mutationFn: deleteConversation,
    onSuccess: (_, uuid) => {
      removeConversation(uuid)
      if (activeConversationId === uuid) {
        setActiveConversation(null)
      }
      queryClient.invalidateQueries({ queryKey: ['conversations'] })
      toast.success('Conversation deleted')
    },
    onError: () => {
      toast.error('Failed to delete conversation')
    },
  })

  const handleNewChat = () => {
    createConversationMutation.mutate({
      title: 'New Conversation',
      model: settings.defaultModel,
      temperature: settings.temperature,
      top_p: settings.topP,
      top_k: settings.topK,
      max_tokens: settings.maxTokens,
    })
  }

  const handleSelectConversation = (uuid: string) => {
    setActiveConversation(uuid)
  }

  const handleDeleteConversation = (uuid: string) => {
    deleteConversationMutation.mutate(uuid)
  }

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isGenerating) return

    setIsGenerating(true)
    setStreamingContent('')

    try {
      if (settings.streamResponses) {
        const conversationId = await sendMessageStream(
          {
            conversation_id: activeConversationId || undefined,
            message: content,
            model: settings.defaultModel,
            temperature: settings.temperature,
            top_p: settings.topP,
            top_k: settings.topK,
            max_tokens: settings.maxTokens,
          },
          (chunk, done) => {
            if (!done) {
              appendStreamingContent(chunk)
            }
          }
        )

        if (!activeConversationId) {
          setActiveConversation(conversationId)
        }
      } else {
        const response = await sendMessage({
          conversation_id: activeConversationId || undefined,
          message: content,
          model: settings.defaultModel,
          temperature: settings.temperature,
          top_p: settings.topP,
          top_k: settings.topK,
          max_tokens: settings.maxTokens,
        })

        if (!activeConversationId) {
          setActiveConversation(response.conversation_id)
        }
      }

      queryClient.invalidateQueries({ queryKey: ['conversation', activeConversationId] })
      queryClient.invalidateQueries({ queryKey: ['conversations'] })
    } catch (error) {
      console.error('Error sending message:', error)
      toast.error('Failed to send message')
    } finally {
      setIsGenerating(false)
      setStreamingContent('')
    }
  }

  const messages: Message[] = activeConversation?.messages || []

  return (
    <div className="flex h-screen bg-dark-950 overflow-hidden">
      <Sidebar
        onNewChat={handleNewChat}
        onSelectConversation={handleSelectConversation}
        onDeleteConversation={handleDeleteConversation}
      />

      <main
        className={`flex-1 flex flex-col transition-all duration-300 ${
          sidebarOpen ? 'ml-72' : 'ml-0'
        }`}
      >
        <header className="h-16 border-b border-dark-700/50 flex items-center justify-between px-4 bg-dark-900/50 backdrop-blur-xl">
          <div className="flex items-center gap-4">
            {!sidebarOpen && (
              <button
                onClick={() => setSidebarOpen(true)}
                className="p-2 rounded-lg hover:bg-dark-800 text-dark-400 hover:text-dark-100 transition-colors"
              >
                <Menu className="w-5 h-5" />
              </button>
            )}
            <h1 className="text-lg font-semibold text-dark-100">
              {currentView === 'chat' && (activeConversation?.title || 'New Chat')}
              {currentView === 'dashboard' && 'Dashboard'}
              {currentView === 'settings' && 'Settings'}
            </h1>
          </div>
        </header>

        <div className="flex-1 overflow-hidden">
          <AnimatePresence mode="wait">
            {currentView === 'chat' && (
              <div key="chat" className="h-full">
                <Chat
                  messages={messages}
                  onSendMessage={handleSendMessage}
                  isGenerating={isGenerating}
                  streamingContent={streamingContent}
                />
              </div>
            )}
            {currentView === 'dashboard' && (
              <div key="dashboard" className="h-full">
                <Dashboard />
              </div>
            )}
            {currentView === 'settings' && (
              <div key="settings" className="h-full">
                <Settings />
              </div>
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  )
}

export default App
