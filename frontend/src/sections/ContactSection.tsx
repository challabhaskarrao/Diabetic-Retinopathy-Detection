import { motion } from 'motion/react';
import { fadeUpVariant } from '../animations/variants';
import { Mail, ArrowRight } from 'lucide-react';

export const ContactSection = () => {
  return (
    <section id="contact" className="py-24 relative overflow-hidden bg-white">
      {/* Background glow */}
      <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-blue-100/50 blur-[120px] rounded-full pointer-events-none" />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
        <motion.div 
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={fadeUpVariant}
        >
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-50 border border-blue-100 mb-8 shadow-sm">
            <Mail className="w-8 h-8 text-blue-600" />
          </div>
          
          <h2 className="text-3xl md:text-5xl font-bold mb-6 text-slate-900">
            Integrate <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-sky-500">Vision AI</span> into Your Practice
          </h2>
          
          <p className="text-slate-600 text-lg mb-10 max-w-2xl mx-auto">
            Reach out to discuss institutional access, API integration for clinical workflows, or collaborations with ophthalmic research programs.
          </p>
          
          <button className="px-8 py-4 rounded-full bg-blue-600 hover:bg-blue-700 text-white font-medium flex items-center justify-center gap-2 transition-all shadow-[0_4px_14px_0_rgb(37,99,235,0.39)] hover:shadow-[0_6px_20px_rgba(37,99,235,0.23)] hover:-translate-y-0.5 mx-auto group">
            Contact Partnerships
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </button>
        </motion.div>
      </div>
    </section>
  );
};
