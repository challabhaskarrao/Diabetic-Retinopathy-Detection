import { motion } from 'motion/react';
import { fadeUpVariant } from '../animations/variants';
import { ArrowRight, ChevronRight, Eye, ScanSearch, Activity } from 'lucide-react';

export const HeroSection = () => {
  return (
    <section id="home" className="relative min-h-screen flex items-center pt-20 overflow-hidden bg-white">
      {/* Subtle background gradients */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-blue-100/40 rounded-full blur-[140px] pointer-events-none" />
      <div className="absolute bottom-0 right-0 w-[600px] h-[600px] bg-sky-50 rounded-full blur-[120px] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full">
        <div className="grid lg:grid-cols-2 gap-16 items-center">

          {/* ── Left — Copy ── */}
          <motion.div initial="hidden" animate="visible" variants={fadeUpVariant} className="max-w-2xl">

            {/* Platform badge */}
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-50 border border-blue-100 mb-8">
              <span className="flex h-2 w-2 rounded-full bg-blue-600 animate-pulse" />
              <span className="text-sm font-medium text-blue-700 tracking-wide">
                Clinical AI Platform · Ophthalmology
              </span>
            </div>

            <h1 className="text-5xl lg:text-6xl font-bold tracking-tight leading-[1.12] mb-6 text-slate-900">
              Intelligent Ocular<br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-sky-500">
                Screening &amp; Diagnostics
              </span>
            </h1>

            <p className="text-lg text-slate-600 mb-4 max-w-xl leading-relaxed">
              A unified platform of specialised AI agents designed for ophthalmic clinicians, 
              screening programs, and research institutions.
            </p>
            <p className="text-base text-slate-500 mb-10 max-w-xl leading-relaxed">
              Select a diagnostic agent below to begin a structured, evidence-based assessment 
              of retinal, refractive, or neuro-ophthalmic conditions.
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
              <a
                href="#agents"
                className="px-8 py-4 rounded-full bg-blue-600 hover:bg-blue-700 text-white font-medium flex items-center justify-center gap-2 transition-all shadow-[0_4px_14px_0_rgb(37,99,235,0.39)] hover:shadow-[0_6px_20px_rgba(37,99,235,0.23)] hover:-translate-y-0.5"
              >
                View Screening Agents
                <ArrowRight className="w-5 h-5" />
              </a>
              <a
                href="#workflow"
                className="px-8 py-4 rounded-full bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 font-medium flex items-center justify-center gap-2 transition-all shadow-sm"
              >
                How It Works
                <ChevronRight className="w-5 h-5 text-slate-400" />
              </a>
            </div>

            {/* Trust indicators */}
            <div className="mt-12 flex flex-wrap gap-6 text-sm text-slate-500 font-medium">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-emerald-500" />
                HIPAA Compliant
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-blue-500" />
                10 Specialised Agents
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-sky-500" />
                Research Validated
              </div>
            </div>
          </motion.div>

          {/* ── Right — Floating UI mockup ── */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative hidden lg:block"
          >
            <div className="relative w-full aspect-square max-w-[560px] mx-auto">
              <div className="absolute inset-0 flex items-center justify-center">

                {/* Orbiting rings */}
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 32, repeat: Infinity, ease: 'linear' }}
                  className="w-[420px] h-[420px] rounded-full border border-blue-100 border-dashed absolute"
                />
                <motion.div
                  animate={{ rotate: -360 }}
                  transition={{ duration: 44, repeat: Infinity, ease: 'linear' }}
                  className="w-[310px] h-[310px] rounded-full border border-sky-200 border-dotted absolute"
                />

                {/* Soft glow core */}
                <div className="w-44 h-44 bg-gradient-to-br from-blue-200 to-sky-100 rounded-full blur-[28px] opacity-50 absolute animate-pulse" />

                {/* Centre icon */}
                <div className="w-32 h-32 bg-white rounded-full border border-slate-100 shadow-[0_8px_30px_rgba(37,99,235,0.12)] flex items-center justify-center z-10">
                  <Eye className="w-14 h-14 text-blue-600" />
                </div>

                {/* Floating card — top-left */}
                <motion.div
                  animate={{ y: [-14, 14, -14] }}
                  transition={{ duration: 4.5, repeat: Infinity, ease: 'easeInOut' }}
                  className="absolute top-8 left-6 bg-white/90 backdrop-blur-md border border-slate-200 shadow-lg p-4 rounded-2xl z-20 min-w-[160px]"
                >
                  <ScanSearch className="w-7 h-7 text-blue-500 mb-2" />
                  <div className="text-xs text-slate-500 font-medium mb-0.5">Fundus Analysis</div>
                  <div className="text-sm font-bold text-slate-900">98.5% Accuracy</div>
                </motion.div>

                {/* Floating card — bottom-right */}
                <motion.div
                  animate={{ y: [14, -14, 14] }}
                  transition={{ duration: 5.5, repeat: Infinity, ease: 'easeInOut', delay: 1 }}
                  className="absolute bottom-14 right-4 bg-white/90 backdrop-blur-md border border-slate-200 shadow-lg p-4 rounded-2xl z-20 min-w-[160px]"
                >
                  <Activity className="w-7 h-7 text-sky-500 mb-2" />
                  <div className="text-xs text-slate-500 font-medium mb-1">Processing OCT Scan</div>
                  <div className="w-28 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                    <motion.div
                      animate={{ width: ['0%', '100%', '0%'] }}
                      transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
                      className="h-full bg-blue-500 rounded-full"
                    />
                  </div>
                </motion.div>
              </div>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
};
