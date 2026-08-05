import { Eye, Github, Linkedin, Mail } from 'lucide-react';

export const Footer = () => {
  return (
    <footer className="bg-slate-50 border-t border-slate-200 pt-16 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center gap-2.5 mb-4">
              <div className="p-2 bg-blue-100 rounded-lg border border-blue-200">
                <Eye className="w-6 h-6 text-blue-600" />
              </div>
              <span className="text-xl font-bold tracking-tight text-slate-900">
                Vision<span className="text-blue-600"> AI</span>
              </span>
            </div>
            <p className="text-slate-600 max-w-sm leading-relaxed">
              Specialised AI screening agents for ophthalmic diagnostics — built for clinicians, researchers, and healthcare institutions worldwide.
            </p>
            <div className="flex gap-4 mt-6">
              {[Github, Linkedin, Mail].map((Icon, i) => (
                <a
                  key={i}
                  href="#"
                  className="p-2 bg-white border border-slate-200 shadow-sm rounded-full hover:border-blue-300 hover:text-blue-600 text-slate-500 transition-colors"
                >
                  <Icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-slate-900 uppercase tracking-wider mb-4">Platform</h3>
            <ul className="space-y-3 text-sm">
              {['Screening Agents', 'Technology', 'Research', 'API Access'].map(item => (
                <li key={item}>
                  <a href="#" className="text-slate-600 hover:text-blue-600 transition-colors">{item}</a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-slate-900 uppercase tracking-wider mb-4">Legal</h3>
            <ul className="space-y-3 text-sm">
              {['Privacy Policy', 'Terms of Service', 'Medical Disclaimer'].map(item => (
                <li key={item}>
                  <a href="#" className="text-slate-600 hover:text-blue-600 transition-colors">{item}</a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="pt-8 border-t border-slate-200 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-slate-500 text-sm">
            © {new Date().getFullYear()} Vision AI. All rights reserved.
          </p>
          <p className="text-slate-400 text-xs text-center md:text-right max-w-xl">
            Disclaimer: Vision AI screening agents are intended for research and clinical decision support only. They do not replace professional ophthalmic examination, diagnosis, or treatment.
          </p>
        </div>
      </div>
    </footer>
  );
};
