'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

// API Service
const apiService = {
  baseURL: 'http://localhost:8000/api',
  
  async get(endpoint: string) {
    const response = await fetch(`${this.baseURL}${endpoint}`)
    return response.json()
  },
  
  async post(endpoint: string, data: any) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    return response.json()
  }
}

interface ApiStatus {
  status: string
  message: string
  database: string
  apps: string[]
}

interface HelloResponse {
  message: string
  status: string
  data: {
    app: string
    version: string
  }
}

export default function Home() {
  const [apiStatus, setApiStatus] = useState<ApiStatus | null>(null)
  const [helloData, setHelloData] = useState<HelloResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        
        // Test both API endpoints
        const [statusResponse, helloResponse] = await Promise.all([
          apiService.get('/status/'),
          apiService.get('/hello/')
        ])
        
        setApiStatus(statusResponse)
        setHelloData(helloResponse)
        setError(null)
      } catch (err) {
        setError('Failed to connect to Django API. Make sure the Django server is running on http://localhost:8000')
        console.error('API Error:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-50 to-pink-100">
        <div className="max-w-md p-8 bg-white rounded-lg shadow-lg">
          <div className="text-center">
            <div className="text-red-500 text-6xl mb-4">⚠️</div>
            <h1 className="text-2xl font-bold text-gray-900 mb-4">Connection Error</h1>
            <p className="text-gray-600 mb-6">{error}</p>
            <button 
              onClick={() => window.location.reload()} 
              className="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-md transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    )
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
              <div className="ml-4">
                <h1 className="text-xl font-semibold text-gray-900">Wisecool</h1>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Link 
                href="/login" 
                className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                Login
              </Link>
              <Link 
                href="/signup" 
                className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Sign Up
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🎉 Django + Next.js Full-Stack App
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Successfully connected frontend and backend!
          </p>
          
          {/* CTA Buttons */}
          <div className="flex justify-center space-x-4">
            <Link 
              href="/login" 
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              Get Started - Login
            </Link>
            <Link 
              href="/signup" 
              className="bg-white hover:bg-gray-50 text-indigo-600 border border-indigo-600 px-6 py-3 rounded-lg font-medium transition-colors"
            >
              Create Account
            </Link>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {/* API Status Card */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4 flex items-center">
              <span className="text-green-500 mr-2">✅</span>
              API Status
            </h2>
            {apiStatus && (
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="font-medium">Status:</span>
                  <span className="text-green-600 font-semibold">{apiStatus.status}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Database:</span>
                  <span className="text-green-600 font-semibold">{apiStatus.database}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Message:</span>
                  <span className="text-gray-700">{apiStatus.message}</span>
                </div>
                <div className="pt-2">
                  <span className="font-medium">Apps:</span>
                  <div className="mt-1">
                    {apiStatus.apps.map((app, index) => (
                      <span 
                        key={index} 
                        className="inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm mr-2"
                      >
                        {app}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Hello World Card */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4 flex items-center">
              <span className="text-blue-500 mr-2">🌍</span>
              Hello World API
            </h2>
            {helloData && (
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="font-medium">Message:</span>
                  <span className="text-blue-600 font-semibold">{helloData.message}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Status:</span>
                  <span className="text-green-600 font-semibold">{helloData.status}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">App:</span>
                  <span className="text-gray-700">{helloData.data.app}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Version:</span>
                  <span className="text-gray-700">{helloData.data.version}</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* API Endpoints */}
        <div className="mt-12 max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4 flex items-center">
              <span className="text-purple-500 mr-2">🔗</span>
              Available API Endpoints
            </h2>
            <div className="grid gap-2 text-sm">
              <div className="flex">
                <span className="bg-green-100 text-green-800 px-2 py-1 rounded font-mono mr-3">GET</span>
                <span className="font-mono text-gray-700">/api/hello/</span>
                <span className="ml-auto text-gray-500">Hello World endpoint</span>
              </div>
              <div className="flex">
                <span className="bg-green-100 text-green-800 px-2 py-1 rounded font-mono mr-3">GET</span>
                <span className="font-mono text-gray-700">/api/status/</span>
                <span className="ml-auto text-gray-500">API status check</span>
              </div>
              <div className="flex">
                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded font-mono mr-3">POST</span>
                <span className="font-mono text-gray-700">/api/auth/login/</span>
                <span className="ml-auto text-gray-500">User authentication</span>
              </div>
              <div className="flex">
                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded font-mono mr-3">POST</span>
                <span className="font-mono text-gray-700">/api/auth/signup/</span>
                <span className="ml-auto text-gray-500">User registration</span>
              </div>
              <div className="flex">
                <span className="bg-green-100 text-green-800 px-2 py-1 rounded font-mono mr-3">GET</span>
                <span className="font-mono text-gray-700">/api/auth/profile/</span>
                <span className="ml-auto text-gray-500">User profile (auth required)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-12 text-center text-gray-500">
          <p>🚀 Your full-stack application is ready!</p>
          <p className="text-sm mt-2">
            Backend: Django REST API running on 
            <a href="http://localhost:8000" className="text-blue-500 ml-1" target="_blank" rel="noopener noreferrer">
              http://localhost:8000
            </a>
          </p>
          <p className="text-sm">
            Frontend: Next.js running on 
            <a href="http://localhost:3000" className="text-blue-500 ml-1" target="_blank" rel="noopener noreferrer">
              http://localhost:3000
            </a>
          </p>
          <p className="text-sm mt-2">
            <a href="/admin/" target="_blank" className="text-indigo-600 hover:text-indigo-800">
              🔧 Admin Panel
            </a>
          </p>
        </div>
      </div>
    </div>
  )
}