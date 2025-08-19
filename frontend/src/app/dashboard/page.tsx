'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
}

interface ApiStatus {
  status: string
  message: string
  database: string
  apps: string[]
}

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null)
  const [apiStatus, setApiStatus] = useState<ApiStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    // Check if user is logged in
    const userData = localStorage.getItem('user')
    if (!userData) {
      router.push('/login')
      return
    }

    try {
      const parsedUser = JSON.parse(userData)
      setUser(parsedUser)
      fetchApiStatus()
    } catch (error) {
      router.push('/login')
    }
  }, [router])

  const fetchApiStatus = async () => {
    try {
      const response = await fetch('/api/status/')
      if (response.ok) {
        const data = await response.json()
        setApiStatus(data)
      }
    } catch (error) {
      console.error('Failed to fetch API status:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = async () => {
    try {
      await fetch('/api/auth/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      })
    } catch (error) {
      console.error('Logout request failed:', error)
    } finally {
      localStorage.removeItem('user')
      router.push('/login')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-8 w-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                  <span className="text-white text-sm font-bold">W</span>
                </div>
              </div>
              <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4">
                  <Link href="/dashboard" className="bg-indigo-700 text-white px-3 py-2 rounded-md text-sm font-medium">
                    Dashboard
                  </Link>
                  <Link href="#" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                    Projects
                  </Link>
                  <Link href="#" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                    Settings
                  </Link>
                </div>
              </div>
            </div>
            <div className="flex items-center">
              <div className="flex items-center space-x-4">
                <span className="text-gray-700 text-sm">
                  Welcome, {user.first_name || user.username}!
                </span>
                <button
                  onClick={handleLogout}
                  className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md text-sm font-medium"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            🎓 Wisecool Parent Dashboard
          </h1>
          <p className="mt-2 text-gray-600">
            Welcome to your full-stack Django + Next.js application
          </p>
        </div>

        {/* User Info Card */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center">
              <div className="bg-green-100 rounded-full w-12 h-12 flex items-center justify-center">
                <span className="text-green-600 text-xl">👤</span>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">User Profile</h3>
                <p className="text-gray-600">{user.email}</p>
              </div>
            </div>
            <div className="mt-4 space-y-2">
              <div className="text-sm">
                <span className="font-medium text-gray-700">ID:</span> {user.id}
              </div>
              <div className="text-sm">
                <span className="font-medium text-gray-700">Username:</span> {user.username}
              </div>
              <div className="text-sm">
                <span className="font-medium text-gray-700">Name:</span> {user.first_name} {user.last_name}
              </div>
            </div>
          </div>

          {/* API Status Card */}
          {apiStatus && (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex items-center">
                <div className="bg-blue-100 rounded-full w-12 h-12 flex items-center justify-center">
                  <span className="text-blue-600 text-xl">🔗</span>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">API Status</h3>
                  <p className="text-green-600 font-medium">{apiStatus.status}</p>
                </div>
              </div>
              <div className="mt-4 space-y-2">
                <div className="text-sm">
                  <span className="font-medium text-gray-700">Database:</span> {apiStatus.database}
                </div>
                <div className="text-sm">
                  <span className="font-medium text-gray-700">Message:</span> {apiStatus.message}
                </div>
              </div>
            </div>
          )}

          {/* Quick Actions Card */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center">
              <div className="bg-purple-100 rounded-full w-12 h-12 flex items-center justify-center">
                <span className="text-purple-600 text-xl">⚡</span>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">Quick Actions</h3>
                <p className="text-gray-600">Admin & API</p>
              </div>
            </div>
            <div className="mt-4 space-y-3">
              <a
                href="/admin/"
                target="_blank"
                rel="noopener noreferrer"
                className="block w-full bg-indigo-600 text-white text-center py-2 px-4 rounded-lg hover:bg-indigo-700 transition-colors text-sm"
              >
                🔧 Admin Panel
              </a>
              <a
                href="/api/status/"
                target="_blank"
                rel="noopener noreferrer"
                className="block w-full bg-green-600 text-white text-center py-2 px-4 rounded-lg hover:bg-green-700 transition-colors text-sm"
              >
                📊 API Status
              </a>
            </div>
          </div>
        </div>

        {/* API Endpoints */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4 flex items-center">
            <span className="text-purple-500 mr-2">🔗</span>
            Available API Endpoints
          </h2>
          <div className="grid gap-3">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center">
                <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-mono mr-3">GET</span>
                <span className="font-mono text-gray-700">/api/hello/</span>
              </div>
              <span className="text-gray-500 text-sm">Hello World endpoint</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center">
                <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-mono mr-3">GET</span>
                <span className="font-mono text-gray-700">/api/status/</span>
              </div>
              <span className="text-gray-500 text-sm">API status check</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center">
                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-mono mr-3">POST</span>
                <span className="font-mono text-gray-700">/api/auth/login/</span>
              </div>
              <span className="text-gray-500 text-sm">User authentication</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center">
                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-mono mr-3">POST</span>
                <span className="font-mono text-gray-700">/api/auth/signup/</span>
              </div>
              <span className="text-gray-500 text-sm">User registration</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center">
                <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-mono mr-3">GET</span>
                <span className="font-mono text-gray-700">/api/auth/profile/</span>
              </div>
              <span className="text-gray-500 text-sm">User profile (auth required)</span>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-12 text-center text-gray-500">
          <p>🚀 Your Django + Next.js full-stack application is running perfectly!</p>
          <p className="text-sm mt-2">
            Backend: Django REST API | Frontend: Next.js with TypeScript
          </p>
        </div>
      </div>
    </div>
  )
}
