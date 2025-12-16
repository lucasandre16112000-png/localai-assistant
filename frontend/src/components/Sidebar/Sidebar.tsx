/**
 * LocalAI Assistant - Sidebar Component
 * Modern sidebar with conversation list and navigation
 * Author: Lucas Andre S
 */

import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  MessageSquare,
  LayoutDashboard,
  Settings,
  Plus,
  Search,
  Pin,
  Trash2,
  ChevronLeft,
  Bot,
  Sparkles,
} from 'lucide-react'
import { useStore, type Conversation } from '../../lib/store'
import { cn, formatRelativeTime, truncate } from '../../lib/utils'
import { Button } from '../ui/Button'

interface SidebarProps {
  onNewChat: () => void
  onSelectConversation: (uuid: string) => void
  onDeleteConversation: (uuid: string) => void
}

export const Sidebar: React.FC<SidebarProps> = ({
  onNewChat,
  onSelectConversation,
  onDeleteConversation,
}) => {
  const {
    sidebarOpen,
    setSidebarOpen,
    currentView,
    setCurrentView,
    conversations,
    activeConversationId,
  } = useStore()

  const [searchQuery, setSearchQuery] = React.useState('')
  const [hoveredId, setHoveredId] = React.useState<string | null>(null)

  const filteredConversations = React.useMemo(() => {
    if (!searchQuery) return conversations
    return conversations.filter((c) =>
      c.title.toLowerCase().includes(searchQuery.toLowerCase())
    )
  }, [conversations, searchQuery])

  const pinnedConversations = filteredConversations.filter((c) => c.is_pinned)
  const regularConversations = filteredConversations.filter((c) => !c.is_pinned)

  return (
    <AnimatePresence>
      {sidebarOpen && (
        <motion.aside
          initial={{ x: -280, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: -280, opacity: 0 }}
          transition={{ type: 'spring', damping: 25, stiffness: 200 }}
          className="fixed left-0 top-0 bottom-0 w-72 bg-dark-900/95 backdrop-blur-xl border-r border-dark-700/50 z-40 flex flex-col"
        >
          <div className="p-4 border-b border-dark-700/50">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center">
                  <Bot className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="font-bold text-dark-100">LocalAI</h1>
                  <p className="text-xs text-dark-400">Premium Assistant</p>
                </div>
              </div>
              <button
                onClick={() => setSidebarOpen(false)}
                className="p-2 rounded-lg hover:bg-dark-800 text-dark-400 hover:text-dark-100 transition-colors"
              >
                <ChevronLeft className="w-5 h-5" />
              </button>
            </div>

            <Button
              variant="glow"
              size="lg"
              className="w-full justify-center"
              onClick={onNewChat}
              icon={<Plus className="w-5 h-5" />}
            >
              New Chat
            </Button>
          </div>

          <div className="p-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-dark-400" />
              <input
                type="text"
                placeholder="Search conversations..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="input-modern pl-10 py-2 text-sm"
              />
            </div>
          </div>

          <nav className="px-3 mb-4">
            <button
              onClick={() => setCurrentView('dashboard')}
              className={cn('sidebar-item w-full', currentView === 'dashboard' && 'active')}
            >
              <LayoutDashboard className="w-5 h-5" />
              <span>Dashboard</span>
            </button>
            <button
              onClick={() => setCurrentView('chat')}
              className={cn('sidebar-item w-full', currentView === 'chat' && 'active')}
            >
              <MessageSquare className="w-5 h-5" />
              <span>Chat</span>
            </button>
            <button
              onClick={() => setCurrentView('settings')}
              className={cn('sidebar-item w-full', currentView === 'settings' && 'active')}
            >
              <Settings className="w-5 h-5" />
              <span>Settings</span>
            </button>
          </nav>

          <div className="flex-1 overflow-y-auto px-3 pb-4 no-scrollbar">
            {pinnedConversations.length > 0 && (
              <div className="mb-4">
                <h3 className="text-xs font-medium text-dark-400 uppercase tracking-wider px-3 mb-2 flex items-center gap-2">
                  <Pin className="w-3 h-3" />
                  Pinned
                </h3>
                {pinnedConversations.map((conv) => (
                  <ConversationItem
                    key={conv.uuid}
                    conversation={conv}
                    isActive={activeConversationId === conv.uuid}
                    isHovered={hoveredId === conv.uuid}
                    onSelect={() => onSelectConversation(conv.uuid)}
                    onDelete={() => onDeleteConversation(conv.uuid)}
                    onHover={setHoveredId}
                  />
                ))}
              </div>
            )}

            <div>
              <h3 className="text-xs font-medium text-dark-400 uppercase tracking-wider px-3 mb-2 flex items-center gap-2">
                <Sparkles className="w-3 h-3" />
                Recent
              </h3>
              {regularConversations.length === 0 ? (
                <p className="text-sm text-dark-500 text-center py-8">
                  No conversations yet
                </p>
              ) : (
                regularConversations.map((conv) => (
                  <ConversationItem
                    key={conv.uuid}
                    conversation={conv}
                    isActive={activeConversationId === conv.uuid}
                    isHovered={hoveredId === conv.uuid}
                    onSelect={() => onSelectConversation(conv.uuid)}
                    onDelete={() => onDeleteConversation(conv.uuid)}
                    onHover={setHoveredId}
                  />
                ))
              )}
            </div>
          </div>

          <div className="p-4 border-t border-dark-700/50">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center text-white text-sm font-medium">
                L
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-dark-100 truncate">Lucas Andre S</p>
                <p className="text-xs text-dark-400">Developer</p>
              </div>
            </div>
          </div>
        </motion.aside>
      )}
    </AnimatePresence>
  )
}

interface ConversationItemProps {
  conversation: Conversation
  isActive: boolean
  isHovered: boolean
  onSelect: () => void
  onDelete: () => void
  onHover: (id: string | null) => void
}

const ConversationItem: React.FC<ConversationItemProps> = ({
  conversation,
  isActive,
  isHovered,
  onSelect,
  onDelete,
  onHover,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn(
        'group relative flex items-center gap-3 px-3 py-2.5 rounded-xl cursor-pointer transition-all duration-200',
        isActive
          ? 'bg-primary-500/10 border border-primary-500/30'
          : 'hover:bg-dark-800/50'
      )}
      onClick={onSelect}
      onMouseEnter={() => onHover(conversation.uuid)}
      onMouseLeave={() => onHover(null)}
    >
      <MessageSquare
        className={cn(
          'w-4 h-4 flex-shrink-0',
          isActive ? 'text-primary-400' : 'text-dark-400'
        )}
      />
      <div className="flex-1 min-w-0">
        <p
          className={cn(
            'text-sm truncate',
            isActive ? 'text-primary-100 font-medium' : 'text-dark-200'
          )}
        >
          {truncate(conversation.title, 25)}
        </p>
        <p className="text-xs text-dark-500">
          {formatRelativeTime(conversation.updated_at)}
        </p>
      </div>
      
      <AnimatePresence>
        {isHovered && (
          <motion.button
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            onClick={(e) => {
              e.stopPropagation()
              onDelete()
            }}
            className="p-1.5 rounded-lg hover:bg-red-500/20 text-dark-400 hover:text-red-400 transition-colors"
          >
            <Trash2 className="w-4 h-4" />
          </motion.button>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

export default Sidebar
