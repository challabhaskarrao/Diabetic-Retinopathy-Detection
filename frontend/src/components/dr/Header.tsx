import React, { useState, useEffect } from "react";
import { Activity, ShieldCheck } from "lucide-react";

const Header: React.FC = () => {
  const [currentDate, setCurrentDate] = useState("");

  useEffect(() => {
    const updateDate = () => {
      const now = new Date();
      const options: Intl.DateTimeFormatOptions = { 
        weekday: 'short', 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      };
      setCurrentDate(now.toLocaleDateString('en-US', options));
    };
    
    updateDate();
    const interval = setInterval(updateDate, 60000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm no-print">
      <div className="app-container py-3">
        <div className="flex items-center justify-between">
          
          {/* Left: Branding */}
          <div className="flex items-center gap-4">
            <div className="bg-blue-600 p-2 rounded flex items-center justify-center">
              <Activity className="w-6 h-6 text-white" aria-hidden="true" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-gray-900 leading-tight">Diabetic Retinopathy AI Screening</h1>
              <p className="text-xs text-gray-500 font-medium">AI-assisted retinal diagnosis</p>
            </div>
          </div>

          {/* Right: System Status */}
          <div className="flex items-center gap-6">
            <div className="hidden md:block text-right">
              <p className="text-xs font-semibold text-gray-700">{currentDate}</p>
              <p className="text-xs text-gray-500">Model: EN-B3-DR-v1.0</p>
            </div>
            
            <div className="flex items-center gap-2 bg-green-50 px-3 py-1.5 rounded-full border border-green-200">
              <div className="w-2 h-2 rounded-full bg-green-600 animate-pulse"></div>
              <span className="text-xs font-bold text-green-700">System Online</span>
            </div>
          </div>
          
        </div>
      </div>
    </header>
  );
};

export default Header;
