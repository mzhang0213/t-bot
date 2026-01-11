'use client';

import { useState } from 'react';
import Map from "@/components/Map";
import Navbar from "@/components/Navbar";

export default function Home() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-black relative">
      {/* Navbar Component */}
      <Navbar onMenuToggle={setSidebarOpen} />

      {/* Sidebar Menu */}
      <div className={`fixed top-0 right-0 h-full w-80 bg-white dark:bg-zinc-900 shadow-2xl transform transition-transform duration-300 ease-in-out z-40 ${
        sidebarOpen ? 'translate-x-0' : 'translate-x-full'
      }`}>
        <div className="p-6 pt-20">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-2xl font-bold text-black dark:text-white">Map Options</h2>
            <button 
              onClick={() => setSidebarOpen(false)}
              className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-zinc-800"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-black dark:text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-black dark:text-white mb-3">Layers</h3>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input type="checkbox" className="mr-2 rounded" defaultChecked />
                  <span className="text-gray-700 dark:text-gray-300">Train Routes</span>
                </label>
                <label className="flex items-center">
                  <input type="checkbox" className="mr-2 rounded" defaultChecked />
                  <span className="text-gray-700 dark:text-gray-300">Bus Routes</span>
                </label>
                <label className="flex items-center">
                  <input type="checkbox" className="mr-2 rounded" />
                  <span className="text-gray-700 dark:text-gray-300">Stops</span>
                </label>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-black dark:text-white mb-3">Display Options</h3>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm text-gray-600 dark:text-gray-400 mb-1">Map Style</label>
                  <select className="w-full p-2 rounded border border-gray-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-black dark:text-white">
                    <option>Standard</option>
                    <option>Satellite</option>
                    <option>Terrain</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm text-gray-600 dark:text-gray-400 mb-1">Zoom Level</label>
                  <input type="range" min="1" max="18" defaultValue="13" className="w-full" />
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-black dark:text-white mb-3">Data Sources</h3>
              <div className="space-y-2">
                <button className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
                  Refresh Data
                </button>
                <button className="w-full py-2 px-4 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors">
                  Load MBTA Routes
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-30 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        ></div>
      )}

      {/* Main Content - Full screen map */}
      <main className="h-screen">
        <div className="w-full h-full">
          <Map />
        </div>
      </main>
    </div>
  );
}