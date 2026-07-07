import React, { useCallback } from "react";
import { UploadCloud, Image as ImageIcon, Trash2, RefreshCw } from "lucide-react";

interface ImageUploaderProps {
  imageFile: File | null;
  imagePreviewUrl: string | null;
  onImageChange: (file: File | null, previewUrl: string | null, base64: string | null) => void;
}

const ImageUploader: React.FC<ImageUploaderProps> = ({
  imageFile,
  imagePreviewUrl,
  onImageChange,
}) => {
  const processFile = (file: File) => {
    if (!file.type.startsWith("image/")) {
      alert("Please upload a valid image file.");
      return;
    }
    
    // Check size (e.g. max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert("Image size exceeds 10MB limit.");
      return;
    }

    const previewUrl = URL.createObjectURL(file);
    const reader = new FileReader();
    reader.onload = () => {
      const base64String = reader.result as string;
      onImageChange(file, previewUrl, base64String);
    };
    reader.readAsDataURL(file);
  };

  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.add('border-blue-500', 'bg-blue-50');
  }, []);

  const onDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('border-blue-500', 'bg-blue-50');
  }, []);

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('border-blue-500', 'bg-blue-50');
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      processFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      processFile(e.target.files[0]);
    }
  };

  const handleRemove = () => {
    onImageChange(null, null, null);
  };

  return (
    <div className="premium-card mb-6">
      <div className="premium-card-header">
        <div className="flex items-center gap-2">
          <ImageIcon className="w-5 h-5 text-blue-600" />
          <span>Retinal Image Upload</span>
        </div>
      </div>
      
      <div className="premium-card-body">
        {!imagePreviewUrl ? (
          <div 
            className="border-2 border-dashed border-gray-300 rounded-lg p-10 text-center hover:bg-gray-50 hover:border-blue-400 transition-all cursor-pointer bg-gray-50/50"
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
            onClick={() => document.getElementById("retinal-upload")?.click()}
          >
            <input 
              type="file" 
              id="retinal-upload" 
              className="hidden" 
              accept="image/jpeg, image/png, image/jpg"
              onChange={handleFileChange}
            />
            <div className="flex justify-center mb-4">
              <div className="bg-white p-3 rounded-full shadow-sm border border-gray-100">
                <UploadCloud className="w-8 h-8 text-blue-500" />
              </div>
            </div>
            <p className="text-sm font-semibold text-gray-900 mb-1">Drag and drop retinal image here</p>
            <p className="text-xs text-gray-500 mb-4">or click to browse your files</p>
            
            <div className="flex items-center justify-center gap-4 text-xs text-gray-400 font-medium">
              <span>Supported: JPEG, PNG</span>
              <span>•</span>
              <span>Max size: 10MB</span>
            </div>
          </div>
        ) : (
          <div className="flex flex-col sm:flex-row items-center gap-6">
            <div className="w-48 h-48 rounded-lg overflow-hidden border border-gray-200 bg-black flex-shrink-0">
              <img src={imagePreviewUrl} alt="Retinal scan" className="w-full h-full object-contain" />
            </div>
            
            <div className="flex-1 w-full">
              <h4 className="text-sm font-semibold text-gray-900 mb-1 truncate">{imageFile?.name}</h4>
              <p className="text-xs text-gray-500 mb-6">
                {(imageFile?.size ? imageFile.size / (1024 * 1024) : 0).toFixed(2)} MB • {imageFile?.type}
              </p>
              
              <div className="flex gap-3">
                <button 
                  onClick={() => document.getElementById("retinal-retake")?.click()}
                  className="btn-secondary text-sm py-2"
                >
                  <RefreshCw className="w-4 h-4" /> Retake
                </button>
                <input 
                  type="file" 
                  id="retinal-retake" 
                  className="hidden" 
                  accept="image/jpeg, image/png, image/jpg"
                  onChange={handleFileChange}
                />
                
                <button 
                  onClick={handleRemove}
                  className="btn-secondary text-red-600 hover:text-red-700 hover:bg-red-50 hover:border-red-200 text-sm py-2"
                >
                  <Trash2 className="w-4 h-4" /> Remove
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageUploader;
