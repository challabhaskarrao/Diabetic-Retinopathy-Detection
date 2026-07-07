import React from "react";
import { ShieldAlert } from "lucide-react";

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white border-t border-gray-200 mt-12 py-6 no-print">
      <div className="app-container">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          
          <div>
            <p className="text-xs text-gray-500 font-medium">
              &copy; {currentYear} Ophthalmology AI Platform. All rights reserved.
            </p>
            <div className="flex gap-4 mt-2">
              <a href="#" className="text-xs text-blue-600 hover:underline">Privacy Policy</a>
              <a href="#" className="text-xs text-blue-600 hover:underline">Terms of Service</a>
              <a href="#" className="text-xs text-blue-600 hover:underline">Support</a>
            </div>
          </div>
          
          <div className="flex items-start gap-2 max-w-sm text-right">
            <ShieldAlert className="w-4 h-4 text-gray-400 mt-0.5 flex-shrink-0" />
            <p className="text-xs text-gray-500 leading-relaxed text-left">
              This software is intended for screening and decision-support purposes only. 
              Final diagnosis must be confirmed by a qualified ophthalmologist.
            </p>
          </div>
          
        </div>
      </div>
    </footer>
  );
};

export default Footer;
