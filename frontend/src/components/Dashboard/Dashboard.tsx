/**
 * LocalAI Assistant - Dashboard Component
 * Premium analytics dashboard with charts and statistics
 * Author: Lucas Andre S
 */

import React from 'react'
import { motion } from 'framer-motion'
import {
  MessageSquare,
  Zap,
  Clock,
  TrendingUp,
  Bot,
  Activity,
  BarChart3,
  ArrowUpRight,
  Sparkles,
} from 'lucide-react'
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart as RechartsPie,
  Pie,
  Cell,
  BarChart,
  Bar,
} from 'recharts'
import { useQuery } from '@tanstack/react-query'
import { getDashboardStats, type DashboardStats } from '../../lib/api'
import { formatNumber } from '../../lib/utils'

const activityData = [
  { name: 'Mon', messages: 45, tokens: 12000 },
  { name: 'Tue', messages: 52, tokens: 15000 },
  { name: 'Wed', messages: 38, tokens: 9500 },
  { name: 'Thu', messages: 65, tokens: 18000 },
  { name: 'Fri', messages: 48, tokens: 14000 },
  { name: 'Sat', messages: 32, tokens: 8000 },
  { name: 'Sun', messages: 28, tokens: 7000 },
]

const modelUsageData = [
  { name: 'dolphin-mistral', value: 45, color: '#0ea5e9' },
  { name: 'codellama', value: 25, color: '#d946ef' },
  { name: 'wizardlm', value: 20, color: '#22c55e' },
  { name: 'nous-hermes', value: 10, color: '#f59e0b' },
]

const hourlyData = Array.from({ length: 24 }, (_, i) => ({
  hour: `${i}:00`,
  messages: Math.floor(Math.random() * 20) + 5,
}))

export const Dashboard: React.FC = () => {
  const { data: stats } = useQuery<DashboardStats>({
    queryKey: ['dashboard-stats'],
    queryFn: getDashboardStats,
    refetchInterval: 30000,
  })

  const defaultStats: DashboardStats = {
    total_conversations: 0,
    total_messages: 0,
    total_tokens: 0,
    average_response_time: 0,
    models_used: {},
    active_model: 'dolphin-mistral',
    avg_response_time: 0,
    conversations_today: 0,
    messages_today: 0,
    tokens_today: 0,
  }

  const displayStats = stats || defaultStats

  return (
    <div className="p-6 space-y-6 overflow-y-auto h-full">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold gradient-text">Dashboard</h1>
          <p className="text-dark-400 mt-1">Monitor your AI assistant usage and performance</p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 glass-card">
          <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
          <span className="text-sm text-dark-300">System Online</span>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Conversations"
          value={formatNumber(displayStats.total_conversations)}
          change={displayStats.conversations_today}
          changeLabel="today"
          icon={<MessageSquare className="w-6 h-6" />}
          color="primary"
          delay={0}
        />
        <StatCard
          title="Total Messages"
          value={formatNumber(displayStats.total_messages)}
          change={displayStats.messages_today}
          changeLabel="today"
          icon={<Zap className="w-6 h-6" />}
          color="accent"
          delay={0.1}
        />
        <StatCard
          title="Tokens Used"
          value={formatNumber(displayStats.total_tokens)}
          change={displayStats.tokens_today}
          changeLabel="today"
          icon={<Activity className="w-6 h-6" />}
          color="green"
          delay={0.2}
        />
        <StatCard
          title="Avg Response Time"
          value={`${(displayStats.avg_response_time || displayStats.average_response_time || 0).toFixed(2)}s`}
          icon={<Clock className="w-6 h-6" />}
          color="yellow"
          delay={0.3}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="lg:col-span-2 glass-card p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-semibold text-dark-100">Weekly Activity</h3>
              <p className="text-sm text-dark-400">Messages and tokens over the past week</p>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-primary-500" />
                <span className="text-xs text-dark-400">Messages</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-accent-500" />
                <span className="text-xs text-dark-400">Tokens</span>
              </div>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={activityData}>
              <defs>
                <linearGradient id="colorMessages" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="colorTokens" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#d946ef" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#d946ef" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="name" stroke="#64748b" fontSize={12} />
              <YAxis stroke="#64748b" fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '1px solid #334155',
                  borderRadius: '12px',
                }}
                labelStyle={{ color: '#f1f5f9' }}
              />
              <Area
                type="monotone"
                dataKey="messages"
                stroke="#0ea5e9"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorMessages)"
              />
              <Area
                type="monotone"
                dataKey="tokens"
                stroke="#d946ef"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorTokens)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="glass-card p-6"
        >
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-dark-100">Model Usage</h3>
            <p className="text-sm text-dark-400">Distribution by model</p>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <RechartsPie>
              <Pie
                data={modelUsageData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
              >
                {modelUsageData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '1px solid #334155',
                  borderRadius: '12px',
                }}
              />
            </RechartsPie>
          </ResponsiveContainer>
          <div className="space-y-2 mt-4">
            {modelUsageData.map((model) => (
              <div key={model.name} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: model.color }}
                  />
                  <span className="text-sm text-dark-300">{model.name}</span>
                </div>
                <span className="text-sm font-medium text-dark-100">{model.value}%</span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="glass-card p-6"
        >
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-dark-100">Hourly Activity</h3>
            <p className="text-sm text-dark-400">Messages per hour today</p>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={hourlyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="hour" stroke="#64748b" fontSize={10} interval={3} />
              <YAxis stroke="#64748b" fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '1px solid #334155',
                  borderRadius: '12px',
                }}
              />
              <Bar dataKey="messages" fill="#0ea5e9" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="glass-card p-6"
        >
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-dark-100">Quick Stats</h3>
            <p className="text-sm text-dark-400">Key performance indicators</p>
          </div>
          <div className="space-y-4">
            <QuickStatItem
              label="Active Model"
              value={displayStats.active_model || 'dolphin-mistral'}
              icon={<Bot className="w-5 h-5 text-primary-400" />}
            />
            <QuickStatItem
              label="Avg Tokens per Message"
              value={displayStats.total_messages > 0 
                ? Math.round(displayStats.total_tokens / displayStats.total_messages).toString()
                : '0'}
              icon={<BarChart3 className="w-5 h-5 text-accent-400" />}
            />
            <QuickStatItem
              label="Messages per Conversation"
              value={displayStats.total_conversations > 0
                ? (displayStats.total_messages / displayStats.total_conversations).toFixed(1)
                : '0'}
              icon={<TrendingUp className="w-5 h-5 text-green-400" />}
            />
            <QuickStatItem
              label="System Status"
              value="Operational"
              icon={<Sparkles className="w-5 h-5 text-yellow-400" />}
              valueColor="text-green-400"
            />
          </div>
        </motion.div>
      </div>
    </div>
  )
}

interface StatCardProps {
  title: string
  value: string
  change?: number
  changeLabel?: string
  icon: React.ReactNode
  color: 'primary' | 'accent' | 'green' | 'yellow'
  delay: number
}

const colorClasses = {
  primary: 'from-primary-500/20 to-primary-500/5 border-primary-500/30',
  accent: 'from-accent-500/20 to-accent-500/5 border-accent-500/30',
  green: 'from-green-500/20 to-green-500/5 border-green-500/30',
  yellow: 'from-yellow-500/20 to-yellow-500/5 border-yellow-500/30',
}

const iconColorClasses = {
  primary: 'text-primary-400 bg-primary-500/20',
  accent: 'text-accent-400 bg-accent-500/20',
  green: 'text-green-400 bg-green-500/20',
  yellow: 'text-yellow-400 bg-yellow-500/20',
}

const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  change,
  changeLabel,
  icon,
  color,
  delay,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className={`glass-card p-6 bg-gradient-to-br ${colorClasses[color]}`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-dark-400 mb-1">{title}</p>
          <p className="text-3xl font-bold text-dark-100">{value}</p>
          {change !== undefined && (
            <div className="flex items-center gap-1 mt-2">
              <ArrowUpRight className="w-4 h-4 text-green-400" />
              <span className="text-sm text-green-400">+{change}</span>
              <span className="text-sm text-dark-500">{changeLabel}</span>
            </div>
          )}
        </div>
        <div className={`p-3 rounded-xl ${iconColorClasses[color]}`}>
          {icon}
        </div>
      </div>
    </motion.div>
  )
}

interface QuickStatItemProps {
  label: string
  value: string
  icon: React.ReactNode
  valueColor?: string
}

const QuickStatItem: React.FC<QuickStatItemProps> = ({
  label,
  value,
  icon,
  valueColor = 'text-dark-100',
}) => {
  return (
    <div className="flex items-center justify-between p-3 rounded-xl bg-dark-800/50">
      <div className="flex items-center gap-3">
        {icon}
        <span className="text-sm text-dark-300">{label}</span>
      </div>
      <span className={`text-sm font-medium ${valueColor}`}>{value}</span>
    </div>
  )
}

export default Dashboard
