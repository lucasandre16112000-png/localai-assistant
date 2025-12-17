/**
 * LocalAI Assistant - Chat Component
 * Modern chat interface with streaming support
 * Author: Lucas Andre S
 */

import React, { useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Send,
  Paperclip,
  StopCircle,
  Copy,
  Check,
  RefreshCw,
  Bot,
  User,
  Sparkles,
} from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { useStore, type Message } from '../../lib/store'
import { cn, copyToClipboard } from '../../lib/utils'
import { Button } from '../ui/Button'
import toast from 'react-hot-toast'

interface ChatProps {
  messages: Message[]
  onSendMessage: (content: string) => void
  isGenerating: boolean
  streamingContent: string
}

export const Chat: React.FC<ChatProps> = ({
  messages,
  onSendMessage,
  isGenerating,
  streamingContent,
}) => {
  const [input, setInput] = React.useState('')
  const [copiedId, setCopiedId] = React.useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)
  const { activeModel } = useStore()

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, streamingContent])

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = 'auto'
      inputRef.current.style.height = `${Math.min(inputRef.current.scrollHeight, 200)}px`
    }
  }, [input])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isGenerating) return
    onSendMessage(input.trim())
    setInput('')
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleCopy = async (content: string, id: string) => {
    const success = await copyToClipboard(content)
    if (success) {
      setCopiedId(id)
      toast.success('Copied to clipboard!')
      setTimeout(() => setCopiedId(null), 2000)
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6">
        {messages.length === 0 && !streamingContent ? (
          <EmptyState />
        ) : (
          <>
            <AnimatePresence>
              {messages.map((message) => (
                <MessageBubble
                  key={message.uuid}
                  message={message}
                  onCopy={handleCopy}
                  isCopied={copiedId === message.uuid}
                />
              ))}
            </AnimatePresence>

            {isGenerating && streamingContent && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex gap-4"
              >
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center flex-shrink-0">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <div className="flex-1 message-bubble message-assistant">
                  <MarkdownContent content={streamingContent} />
                  <span className="inline-block w-2 h-5 bg-primary-400 animate-pulse ml-1" />
                </div>
              </motion.div>
            )}

            {isGenerating && !streamingContent && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex gap-4"
              >
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center flex-shrink-0">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <div className="message-bubble message-assistant">
                  <div className="typing-indicator">
                    <span />
                    <span />
                    <span />
                  </div>
                </div>
              </motion.div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="border-t border-dark-700/50 p-4 bg-dark-900/50 backdrop-blur-xl">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
          <div className="relative">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Send a message..."
              rows={1}
              className="w-full bg-dark-800/50 border border-dark-600 rounded-2xl px-4 py-4 pr-32 text-dark-100 placeholder-dark-400 resize-none focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all duration-200"
              disabled={isGenerating}
            />
            <div className="absolute right-2 bottom-2 flex items-center gap-2">
              <button
                type="button"
                className="p-2 rounded-xl text-dark-400 hover:text-dark-200 hover:bg-dark-700/50 transition-colors"
                title="Attach file"
              >
                <Paperclip className="w-5 h-5" />
              </button>
              <Button
                type="submit"
                variant="glow"
                size="sm"
                disabled={!input.trim() || isGenerating}
                icon={isGenerating ? <StopCircle className="w-4 h-4" /> : <Send className="w-4 h-4" />}
              >
                {isGenerating ? 'Stop' : 'Send'}
              </Button>
            </div>
          </div>
          <p className="text-xs text-dark-500 text-center mt-2">
            Using <span className="text-primary-400 font-medium">{activeModel}</span> • Press Enter to send, Shift+Enter for new line
          </p>
        </form>
      </div>
    </div>
  )
}

const EmptyState: React.FC = () => {
  const suggestions = [
    'Explain quantum computing in simple terms',
    'Write a Python function to sort a list',
    'Help me debug this code',
    'Create a marketing strategy for a startup',
  ]

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex flex-col items-center justify-center h-full text-center px-4"
    >
      <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center mb-6">
        <Sparkles className="w-10 h-10 text-white" />
      </div>
      <h2 className="text-2xl font-bold text-dark-100 mb-2">
        Welcome to LocalAI Assistant
      </h2>
      <p className="text-dark-400 mb-8 max-w-md">
        Your premium AI companion for coding, analysis, writing, and more.
        Start a conversation or try one of these suggestions:
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl">
        {suggestions.map((suggestion, index) => (
          <motion.button
            key={index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="glass-card p-4 text-left text-sm text-dark-300 hover:text-dark-100 hover:border-primary-500/30 transition-all duration-200"
          >
            {suggestion}
          </motion.button>
        ))}
      </div>
    </motion.div>
  )
}

interface MessageBubbleProps {
  message: Message
  onCopy: (content: string, id: string) => void
  isCopied: boolean
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, onCopy, isCopied }) => {
  const isUser = message.role === 'user'

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className={cn('flex gap-4', isUser && 'flex-row-reverse')}
    >
      <div
        className={cn(
          'w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0',
          isUser
            ? 'bg-dark-700'
            : 'bg-gradient-to-br from-primary-500 to-accent-500'
        )}
      >
        {isUser ? (
          <User className="w-5 h-5 text-dark-300" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>

      <div className={cn('flex-1 max-w-[80%]', isUser && 'flex flex-col items-end')}>
        <div className={cn('message-bubble', isUser ? 'message-user' : 'message-assistant')}>
          {isUser ? (
            <p className="whitespace-pre-wrap">{message.content}</p>
          ) : (
            <MarkdownContent content={message.content} />
          )}
        </div>

        {!isUser && (
          <div className="flex items-center gap-2 mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              onClick={() => onCopy(message.content, message.uuid || message.id)}
              className="p-1.5 rounded-lg hover:bg-dark-700 text-dark-400 hover:text-dark-200 transition-colors"
              title="Copy"
            >
              {isCopied ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
            </button>
            <button
              className="p-1.5 rounded-lg hover:bg-dark-700 text-dark-400 hover:text-dark-200 transition-colors"
              title="Regenerate"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        )}

        {!isUser && message.generation_time && (
          <p className="text-xs text-dark-500 mt-1">
            {message.tokens} tokens • {message.generation_time.toFixed(2)}s
          </p>
        )}
      </div>
    </motion.div>
  )
}

const MarkdownContent: React.FC<{ content: string }> = ({ content }) => {
  return (
    <ReactMarkdown
      className="prose prose-invert prose-sm max-w-none"
      components={{
        code({ className, children, ...props }) {
          const match = /language-(\w+)/.exec(className || '')
          const isInline = !match
          return !isInline && match ? (
            <div className="code-block my-4">
              <div className="flex items-center justify-between px-4 py-2 bg-dark-800 border-b border-dark-700">
                <span className="text-xs text-dark-400 font-mono">{match[1]}</span>
                <button
                  onClick={() => copyToClipboard(String(children))}
                  className="text-xs text-dark-400 hover:text-dark-200 transition-colors"
                >
                  Copy
                </button>
              </div>
              <SyntaxHighlighter
                // @ts-ignore - type mismatch in library
                style={oneDark}
                language={match[1]}
                PreTag="div"
                customStyle={{
                  margin: 0,
                  background: 'transparent',
                  padding: '1rem',
                }}
              >
                {String(children).replace(/\n$/, '')}
              </SyntaxHighlighter>
            </div>
          ) : (
            <code className="bg-dark-700 px-1.5 py-0.5 rounded text-primary-300 text-sm" {...props}>
              {children}
            </code>
          )
        },
        p: ({ children }) => <p className="mb-4 last:mb-0">{children}</p>,
        ul: ({ children }) => <ul className="list-disc list-inside mb-4 space-y-1">{children}</ul>,
        ol: ({ children }) => <ol className="list-decimal list-inside mb-4 space-y-1">{children}</ol>,
        h1: ({ children }) => <h1 className="text-xl font-bold mb-4 text-dark-100">{children}</h1>,
        h2: ({ children }) => <h2 className="text-lg font-bold mb-3 text-dark-100">{children}</h2>,
        h3: ({ children }) => <h3 className="text-base font-bold mb-2 text-dark-100">{children}</h3>,
        blockquote: ({ children }) => (
          <blockquote className="border-l-4 border-primary-500 pl-4 my-4 text-dark-300 italic">
            {children}
          </blockquote>
        ),
        a: ({ href, children }) => (
          <a href={href} className="text-primary-400 hover:underline" target="_blank" rel="noopener noreferrer">
            {children}
          </a>
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  )
}

export default Chat
