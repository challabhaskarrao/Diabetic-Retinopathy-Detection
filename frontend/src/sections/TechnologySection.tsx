import { motion } from 'motion/react';
import { fadeUpVariant, staggerContainer } from '../animations/variants';

export const TechnologySection = () => {
  const technologies = [
    "TensorFlow", "PyTorch", "OpenCV", "FastAPI", "Next.js", 
    "React", "Python", "Machine Learning", "Deep Learning", 
    "CNN", "Vision Transformer", "CUDA", "WebGL", "TypeScript"
  ];

  return (
    <section id="technology" className="py-24 bg-slate-50 border-y border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={fadeUpVariant}
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-6 text-slate-900">
              Built on Modern <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-sky-500">Technology Stacks</span>
            </h2>
            <p className="text-slate-600 text-lg mb-8 leading-relaxed">
              We leverage the latest advancements in artificial intelligence and web technologies to deliver a robust, secure, and lightning-fast diagnostic platform. Our inference engines are optimized for maximum throughput and minimum latency.
            </p>
            
            <div className="flex items-center gap-4 text-sm font-medium text-slate-700">
              <div className="flex -space-x-4">
                {/* Abstract visualization of tech nodes */}
                <div className="w-12 h-12 rounded-full bg-white border-2 border-slate-100 shadow-sm flex items-center justify-center text-blue-600 font-bold">TF</div>
                <div className="w-12 h-12 rounded-full bg-white border-2 border-slate-100 shadow-sm flex items-center justify-center text-orange-500 font-bold">PT</div>
                <div className="w-12 h-12 rounded-full bg-white border-2 border-slate-100 shadow-sm flex items-center justify-center text-sky-500 font-bold">Re</div>
              </div>
              <span className="ml-4 text-slate-600">Enterprise-grade architecture</span>
            </div>
          </motion.div>

          <motion.div 
            variants={staggerContainer}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-50px" }}
            className="flex flex-wrap gap-3 justify-center lg:justify-start"
          >
            {technologies.map((tech, i) => (
              <motion.div
                key={i}
                variants={fadeUpVariant}
                whileHover={{ scale: 1.05, y: -2 }}
                className="px-6 py-3 rounded-full bg-white text-slate-700 font-medium border border-slate-200 shadow-sm hover:border-blue-300 hover:bg-blue-50 hover:text-blue-700 transition-all cursor-default"
              >
                {tech}
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  );
};
