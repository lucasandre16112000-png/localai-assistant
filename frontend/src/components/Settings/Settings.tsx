/**
 * LocalAI Assistant - Settings Component
 * Comprehensive settings panel with model configuration
 * Author: Lucas Andre S
 */

import React from 'react'
import { motion } from 'framer-motion'
import {
  Settings as SettingsIcon,
  Bot,
  Palette,
  Sliders,
  Info,
  Moon,
  Sun,
  Save,
  RotateCcw,
  ChevronRight,
  Check,
} from 'lucide-react'
import * as Slider from '@radix-ui/react-slider'
import * as Switch from '@radix-ui/react-switch'
import { useQuery } from '@tanstack/react-query'
import { useStore, type Settings as SettingsType } from '@/lib/store'
import { getModels, getSystemPrompts, type SystemPrompt } from '@/lib/api'
import { Button } from '@/components/ui/Button'
import { cn } from '@/lib/utils'
import toast from 'react-hot-toast'

type SettingsTab = 'general' | 'models' | 'appearance' | 'prompts' | 'about'

export const Settings: React.FC = () => {
  const [activeTab, setActiveTab] = React.useState<SettingsTab>('general')
  const { settings, updateSettings, activeModel, setActiveModel } = useStore()

  const { data: modelsData } = useQuery({
    queryKey: ['models'],
    queryFn: getModels,
  })

  const { data: prompts } = useQuery({
    queryKey: ['system-prompts'],
    queryFn: getSystemPrompts,
  })

  const tabs: { id: SettingsTab; label: string; icon: React.ReactNode }[] = [
    { id: 'general', label: 'General', icon: <SettingsIcon className="w-5 h-5" /> },
    { id: 'models', label: 'Models', icon: <Bot className="w-5 h-5" /> },
    { id: 'appearance', label: 'Appearance', icon: <Palette className="w-5 h-5" /> },
    { id: 'prompts', label: 'System Prompts', icon: <Sliders className="w-5 h-5" /> },
    { id: 'about', label: 'About', icon: <Info className="w-5 h-5" /> },
  ]

  const handleSave = () => {
    toast.success('Settings saved successfully!')
  }

  const handleReset = () => {
    updateSettings({
      temperature: 0.7,
      topP: 0.9,
      topK: 40,
      maxTokens: 2048,
      streamResponses: true,
      autoSave: true,
    })
    toast.success('Settings reset to defaults')
  }

  return (
    <div className="flex h-full">
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className="w-64 border-r border-dark-700/50 p-4"
      >
        <h2 className="text-xl font-bold text-dark-100 mb-6 px-3">Settings</h2>
        <nav className="space-y-1">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={cn(
                'w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm transition-all duration-200',
                activeTab === tab.id
                  ? 'bg-primary-500/10 text-primary-400 font-medium'
                  : 'text-dark-400 hover:text-dark-200 hover:bg-dark-800/50'
              )}
            >
              {tab.icon}
              <span>{tab.label}</span>
              {activeTab === tab.id && (
                <ChevronRight className="w-4 h-4 ml-auto" />
              )}
            </button>
          ))}
        </nav>
      </motion.div>

      <div className="flex-1 overflow-y-auto p-6">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-2xl"
        >
          {activeTab === 'general' && (
            <GeneralSettings
              settings={settings}
              onUpdate={updateSettings}
            />
          )}
          {activeTab === 'models' && (
            <ModelSettings
              models={modelsData?.models || []}
              activeModel={activeModel}
              onSelectModel={setActiveModel}
              settings={settings}
              onUpdate={updateSettings}
            />
          )}
          {activeTab === 'appearance' && (
            <AppearanceSettings
              settings={settings}
              onUpdate={updateSettings}
            />
          )}
          {activeTab === 'prompts' && (
            <PromptsSettings prompts={prompts || []} />
          )}
          {activeTab === 'about' && <AboutSection />}
        </motion.div>

        {activeTab !== 'about' && (
          <div className="flex items-center gap-3 mt-8 pt-6 border-t border-dark-700/50">
            <Button variant="glow" onClick={handleSave} icon={<Save className="w-4 h-4" />}>
              Save Changes
            </Button>
            <Button variant="ghost" onClick={handleReset} icon={<RotateCcw className="w-4 h-4" />}>
              Reset to Defaults
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}

interface GeneralSettingsProps {
  settings: SettingsType
  onUpdate: (settings: Partial<SettingsType>) => void
}

const GeneralSettings: React.FC<GeneralSettingsProps> = ({ settings, onUpdate }) => {
  return (
    <div className="space-y-8">
      <div>
        <h3 className="text-lg font-semibold text-dark-100 mb-4">General Settings</h3>
        <div className="space-y-6">
          <SettingItem
            title="Stream Responses"
            description="Show AI responses as they are generated"
          >
            <Switch.Root
              checked={settings.streamResponses}
              onCheckedChange={(checked) => onUpdate({ streamResponses: checked })}
              className="w-11 h-6 bg-dark-700 rounded-full relative data-[state=checked]:bg-primary-500 transition-colors"
            >
              <Switch.Thumb className="block w-5 h-5 bg-white rounded-full transition-transform translate-x-0.5 data-[state=checked]:translate-x-[22px]" />
            </Switch.Root>
          </SettingItem>

          <SettingItem
            title="Auto Save"
            description="Automatically save conversations"
          >
            <Switch.Root
              checked={settings.autoSave}
              onCheckedChange={(checked) => onUpdate({ autoSave: checked })}
              className="w-11 h-6 bg-dark-700 rounded-full relative data-[state=checked]:bg-primary-500 transition-colors"
            >
              <Switch.Thumb className="block w-5 h-5 bg-white rounded-full transition-transform translate-x-0.5 data-[state=checked]:translate-x-[22px]" />
            </Switch.Root>
          </SettingItem>
        </div>
      </div>
    </div>
  )
}

interface ModelSettingsProps {
  models: { name: string }[]
  activeModel: string
  onSelectModel: (model: string) => void
  settings: SettingsType
  onUpdate: (settings: Partial<SettingsType>) => void
}

const ModelSettings: React.FC<ModelSettingsProps> = ({
  models,
  activeModel,
  onSelectModel,
  settings,
  onUpdate,
}) => {
  return (
    <div className="space-y-8">
      <div>
        <h3 className="text-lg font-semibold text-dark-100 mb-4">Model Selection</h3>
        <div className="grid grid-cols-2 gap-3">
          {models.map((model) => (
            <button
              key={model.name}
              onClick={() => onSelectModel(model.name)}
              className={cn(
                'p-4 rounded-xl border text-left transition-all duration-200',
                activeModel === model.name
                  ? 'border-primary-500 bg-primary-500/10'
                  : 'border-dark-700 hover:border-dark-600 bg-dark-800/50'
              )}
            >
              <div className="flex items-center justify-between">
                <span className="font-medium text-dark-100">{model.name}</span>
                {activeModel === model.name && (
                  <Check className="w-5 h-5 text-primary-400" />
                )}
              </div>
            </button>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold text-dark-100 mb-4">Model Parameters</h3>
        <div className="space-y-6">
          <SliderSetting
            label="Temperature"
            value={settings.temperature}
            min={0}
            max={2}
            step={0.1}
            onChange={(value) => onUpdate({ temperature: value })}
            description="Controls randomness. Lower = more focused, Higher = more creative"
          />
          <SliderSetting
            label="Top P"
            value={settings.topP}
            min={0}
            max={1}
            step={0.05}
            onChange={(value) => onUpdate({ topP: value })}
            description="Nucleus sampling threshold"
          />
          <SliderSetting
            label="Top K"
            value={settings.topK}
            min={1}
            max={100}
            step={1}
            onChange={(value) => onUpdate({ topK: value })}
            description="Limits vocabulary to top K tokens"
          />
          <SliderSetting
            label="Max Tokens"
            value={settings.maxTokens}
            min={256}
            max={8192}
            step={256}
            onChange={(value) => onUpdate({ maxTokens: value })}
            description="Maximum response length"
          />
        </div>
      </div>
    </div>
  )
}

interface AppearanceSettingsProps {
  settings: SettingsType
  onUpdate: (settings: Partial<SettingsType>) => void
}

const AppearanceSettings: React.FC<AppearanceSettingsProps> = ({ settings, onUpdate }) => {
  return (
    <div className="space-y-8">
      <div>
        <h3 className="text-lg font-semibold text-dark-100 mb-4">Theme</h3>
        <div className="grid grid-cols-2 gap-4">
          <button
            onClick={() => onUpdate({ theme: 'dark' })}
            className={cn(
              'p-6 rounded-xl border flex flex-col items-center gap-3 transition-all duration-200',
              settings.theme === 'dark'
                ? 'border-primary-500 bg-primary-500/10'
                : 'border-dark-700 hover:border-dark-600 bg-dark-800/50'
            )}
          >
            <Moon className="w-8 h-8 text-dark-300" />
            <span className="font-medium text-dark-100">Dark Mode</span>
          </button>
          <button
            onClick={() => onUpdate({ theme: 'light' })}
            className={cn(
              'p-6 rounded-xl border flex flex-col items-center gap-3 transition-all duration-200',
              settings.theme === 'light'
                ? 'border-primary-500 bg-primary-500/10'
                : 'border-dark-700 hover:border-dark-600 bg-dark-800/50'
            )}
          >
            <Sun className="w-8 h-8 text-yellow-400" />
            <span className="font-medium text-dark-100">Light Mode</span>
          </button>
        </div>
      </div>
    </div>
  )
}

interface PromptsSettingsProps {
  prompts: SystemPrompt[]
}

const PromptsSettings: React.FC<PromptsSettingsProps> = ({ prompts }) => {
  const [selectedPrompt, setSelectedPrompt] = React.useState<SystemPrompt | null>(null)

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-dark-100 mb-4">System Prompts</h3>
        <p className="text-sm text-dark-400 mb-4">
          Choose a system prompt to customize the AI's behavior and personality.
        </p>
        <div className="space-y-3">
          {prompts.map((prompt) => (
            <button
              key={prompt.id}
              onClick={() => setSelectedPrompt(prompt)}
              className={cn(
                'w-full p-4 rounded-xl border text-left transition-all duration-200',
                selectedPrompt?.id === prompt.id
                  ? 'border-primary-500 bg-primary-500/10'
                  : 'border-dark-700 hover:border-dark-600 bg-dark-800/50'
              )}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-dark-100">{prompt.name}</span>
                {prompt.is_default && (
                  <span className="text-xs px-2 py-1 rounded-full bg-primary-500/20 text-primary-400">
                    Default
                  </span>
                )}
              </div>
              <p className="text-sm text-dark-400">{prompt.description}</p>
            </button>
          ))}
        </div>
      </div>

      {selectedPrompt && (
        <div className="glass-card p-4">
          <h4 className="font-medium text-dark-100 mb-2">Prompt Content</h4>
          <pre className="text-sm text-dark-300 whitespace-pre-wrap bg-dark-800/50 p-4 rounded-xl max-h-60 overflow-y-auto">
            {selectedPrompt.content}
          </pre>
        </div>
      )}
    </div>
  )
}

const AboutSection: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="text-center py-8">
        <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center mx-auto mb-4">
          <Bot className="w-10 h-10 text-white" />
        </div>
        <h2 className="text-2xl font-bold gradient-text mb-2">LocalAI Assistant</h2>
        <p className="text-dark-400">Premium AI Assistant with Local LLM Support</p>
        <p className="text-sm text-dark-500 mt-2">Version 1.0.0</p>
      </div>

      <div className="glass-card p-6 space-y-4">
        <div className="flex justify-between">
          <span className="text-dark-400">Developer</span>
          <span className="text-dark-100 font-medium">Lucas Andre S</span>
        </div>
        <div className="flex justify-between">
          <span className="text-dark-400">GitHub</span>
          <a
            href="https://github.com/lucasandre16112000-png"
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary-400 hover:underline"
          >
            lucasandre16112000-png
          </a>
        </div>
        <div className="flex justify-between">
          <span className="text-dark-400">License</span>
          <span className="text-dark-100">MIT</span>
        </div>
        <div className="flex justify-between">
          <span className="text-dark-400">Built with</span>
          <span className="text-dark-100">React, TypeScript, FastAPI</span>
        </div>
      </div>

      <p className="text-sm text-dark-500 text-center">
        Made with ❤️ for the open-source community
      </p>
    </div>
  )
}

interface SettingItemProps {
  title: string
  description: string
  children: React.ReactNode
}

const SettingItem: React.FC<SettingItemProps> = ({ title, description, children }) => {
  return (
    <div className="flex items-center justify-between p-4 rounded-xl bg-dark-800/50">
      <div>
        <h4 className="font-medium text-dark-100">{title}</h4>
        <p className="text-sm text-dark-400">{description}</p>
      </div>
      {children}
    </div>
  )
}

interface SliderSettingProps {
  label: string
  value: number
  min: number
  max: number
  step: number
  onChange: (value: number) => void
  description: string
}

const SliderSetting: React.FC<SliderSettingProps> = ({
  label,
  value,
  min,
  max,
  step,
  onChange,
  description,
}) => {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <h4 className="font-medium text-dark-100">{label}</h4>
          <p className="text-sm text-dark-400">{description}</p>
        </div>
        <span className="text-lg font-mono text-primary-400">{value}</span>
      </div>
      <Slider.Root
        value={[value]}
        onValueChange={([v]) => onChange(v)}
        min={min}
        max={max}
        step={step}
        className="relative flex items-center w-full h-5"
      >
        <Slider.Track className="relative h-2 flex-grow rounded-full bg-dark-700">
          <Slider.Range className="absolute h-full rounded-full bg-gradient-to-r from-primary-500 to-accent-500" />
        </Slider.Track>
        <Slider.Thumb className="block w-5 h-5 bg-white rounded-full shadow-lg focus:outline-none focus:ring-2 focus:ring-primary-500" />
      </Slider.Root>
    </div>
  )
}

export default Settings
