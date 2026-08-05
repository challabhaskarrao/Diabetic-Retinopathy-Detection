import { motion } from 'motion/react';
import { fadeUpVariant } from '../animations/variants';

export const AboutSection = () => {
  return (
    <section id="about" className="py-24 relative bg-slate-50">
      {/* Abstract Background Element */}
      <div className="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l from-blue-100/50 to-transparent pointer-events-none" />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={fadeUpVariant}
            className="relative h-[400px] rounded-3xl overflow-hidden bg-white shadow-sm border border-slate-200 hidden lg:flex items-center justify-center"
          >
             {/* Tech/Research visual representation */}
             <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMSIgZmlsbD0icmdiYSgwLDAsMCwwLjA1KSIvPjwvc3ZnPg==')] opacity-50" />
             <div className="w-64 h-64 border-4 border-blue-200 rounded-full flex items-center justify-center relative bg-blue-50/50">
                <div className="w-48 h-48 border-4 border-sky-300 rounded-full flex items-center justify-center animate-[spin_10s_linear_infinite]">
                  <div className="w-4 h-4 bg-blue-600 rounded-full absolute -top-2" />
                </div>
                <div className="w-32 h-32 border-4 border-slate-200 rounded-full absolute animate-[spin_15s_linear_infinite_reverse]">
                  <div className="w-3 h-3 bg-sky-500 rounded-full absolute -bottom-1.5 left-1/2 -translate-x-1/2" />
                </div>
             </div>
          </motion.div>

          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={fadeUpVariant}
          >
            <div className="text-sm font-bold tracking-widest text-blue-600 uppercase mb-4">About Vision AI</div>
            <h2 className="text-3xl md:text-5xl font-bold mb-6 text-slate-900">
              Purpose-Built for <span className="text-blue-600">Ophthalmic</span> Practice
            </h2>
            <p className="text-slate-600 text-lg mb-6 leading-relaxed">
              Vision AI is a research-driven clinical platform that consolidates ten specialised AI screening agents into a single, structured interface — purpose-built for ophthalmologists, optometrists, and ophthalmic researchers.
            </p>
            <p className="text-slate-600 text-lg mb-8 leading-relaxed">
              Each agent is trained on large-scale, clinician-annotated ophthalmic datasets and validated against established diagnostic standards. The platform is designed to augment clinical decision-making, accelerate population screening programs, and support evidence-based ophthalmic research globally.
            </p>
            
            <div className="grid grid-cols-2 gap-6 pt-6 border-t border-slate-200">
              <div>
                <div className="text-3xl font-bold text-slate-900 mb-1">10</div>
                <div className="text-sm text-slate-500 font-medium">Screening Agents</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-slate-900 mb-1">99%</div>
                <div className="text-sm text-slate-500 font-medium">Peak Clinical Accuracy</div>
              </div>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
};
