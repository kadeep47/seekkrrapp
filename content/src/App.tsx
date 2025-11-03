import React from 'react'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Welcome to Seeker
          </h1>
          <p className="text-xl text-gray-600">
            Location-based questing platform
          </p>
        </header>
        
        <main className="max-w-2xl mx-auto">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold mb-4">Getting Started</h2>
            <p className="text-gray-700 mb-4">
              This is the foundation of your Seeker platform. The project structure 
              has been set up and you're ready to start building!
            </p>
            <div className="space-y-2">
              <p className="text-sm text-gray-600">
                • Backend API will be available at http://localhost:8000
              </p>
              <p className="text-sm text-gray-600">
                • Web app is running at http://localhost:3000
              </p>
              <p className="text-sm text-gray-600">
                • Mobile app can be developed with Flutter
              </p>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default App