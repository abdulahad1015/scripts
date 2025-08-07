# PDF Text Extractor with Ollama

A comprehensive solution to extract text from PDF files (CVs/resumes) and use Ollama AI to process and structure the extracted data.

## 🚀 Quick Start

### Option 1: Simple Text Extraction (No AI Setup Required)
```bash
python simple_extractor.py
```
This will extract text and basic information (name, email, phone, skills) using pattern matching.

### Option 2: Full AI-Powered Analysis
1. Install Ollama from https://ollama.ai/
2. Run the setup helper: `python ollama_setup.py`
3. Run the main script: `python main.py`

## 📁 Project Structure

```
Ollama_OCR/
├── main.py                    # Main script with Ollama integration
├── simple_extractor.py        # Basic text extraction (no AI required)
├── ollama_setup.py           # Helper to setup Ollama models
├── requirements.txt          # Python dependencies
├── extracted_data.json       # Output from main.py
├── simple_extracted_data.json # Output from simple_extractor.py
└── CVs/                      # Folder containing PDF files
    ├── a.pdf
    ├── Ashar_Resume.pdf
    ├── CV - Muhammad shayan umar.pdf
    ├── Maheer Shakil Resume AI ML Intern - Maheer Shakil[1].pdf
    └── Muhammad Umar Orakzai - Resume.pdf
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.7+
- PDF files in the `CVs` folder

### Installation
```bash
# Install Python packages
pip install -r requirements.txt
```

### For AI Processing (Optional)
1. **Install Ollama**: Download from https://ollama.ai/
2. **Setup Models**: Run `python ollama_setup.py` for guided setup
3. **Manual Setup** (alternative):
   ```bash
   # Install a model (choose one)
   ollama pull llama3.2:1b    # Small, fast (1GB)
   ollama pull llama3.2:3b    # Medium (2GB)
   ollama pull llama3.2       # Full model (4.7GB)
   
   # Start Ollama service
   ollama serve
   ```

## 🎯 Usage

### Basic Text Extraction
```bash
python simple_extractor.py
```
**Output**: Extracts text and basic info using pattern matching
- ✅ Names, emails, phone numbers
- ✅ Detected skills and keywords
- ✅ Text statistics
- ✅ No external dependencies

### AI-Powered Analysis  
```bash
python main.py
```
**Output**: Full structured data extraction using AI
- ✅ Comprehensive information extraction
- ✅ Professional summaries
- ✅ Structured education and experience data
- ✅ Advanced skill categorization

## 📊 Current Results

Successfully processed 5 CV files:

| File | Name | Email | Skills Detected |
|------|------|-------|-----------------|
| a.pdf | Abdul Ahad Danish | abdulahad1015@gmail.com | Python, C++, JavaScript, SQL, Flask |
| Ashar_Resume.pdf | Muhammad Ashar Usmani | ashar.usmani9@gmail.com | Python, C++, SQL, ML, TensorFlow |
| CV - Muhammad shayan umar.pdf | Muhammad Shayan Umar | shayanumarmuhammad@gmail.com | Python, ML, AI, Power BI, SQL |
| Maheer Shakil Resume.pdf | Maheer Shakil | maheershakil24@gmail.com | Python, SQL, ML, AI, Scikit-learn |
| Muhammad Umar Orakzai - Resume.pdf | Muhammad Umar Orakzai | umarorakzai012@gmail.com | Python, Java, C++, AI, Flutter |

## 📋 Extracted Data Fields

### Simple Extractor
- Name (pattern-matched)
- Email address
- Phone number
- Detected skills (keyword matching)
- Text statistics

### AI-Powered Extractor
- Full name
- Contact information
- Education details
- Work experience
- Technical skills
- Professional summary
- Certifications
- Projects

## 🔧 Troubleshooting

### Common Issues

1. **"No text extracted"**
   - PDF might be image-based
   - Consider using OCR tools like pytesseract

2. **"Ollama connection error"**
   - Make sure Ollama is installed
   - Run `ollama serve` to start the service
   - Use `python ollama_setup.py` for guided setup

3. **"Model not found"**
   - Install a model: `ollama pull llama3.2:1b`
   - Check available models: `ollama list`

4. **Large file processing**
   - For many PDFs, consider batch processing
   - Monitor memory usage for large files

## 🚀 Advanced Usage

### Custom Model Selection
```python
from main import PDFTextExtractor

extractor = PDFTextExtractor()
results = extractor.process_all_pdfs(model="mistral")  # Use specific model
```

### Batch Processing
```python
# Process specific files
extractor = PDFTextExtractor("path/to/cvs")
results = extractor.process_all_pdfs()
```

### Custom Prompts
Modify the `process_with_ollama` method in `main.py` to customize extraction prompts.

## 📁 Output Files

- **extracted_data.json**: Complete results with raw text and AI analysis
- **simple_extracted_data.json**: Basic extraction results
- Both files contain structured data for further processing

## 🎨 Customization

- **Change extraction fields**: Modify the prompt in `process_with_ollama()`
- **Add new PDF sources**: Place PDFs in the `CVs` folder
- **Custom output format**: Modify the `save_results()` method
- **Different models**: Use `ollama_setup.py` to install other models

## 📈 Next Steps

1. **Install Ollama** for AI-powered extraction
2. **Run full analysis** with structured data
3. **Integrate with databases** for CV management
4. **Add OCR support** for image-based PDFs
5. **Create web interface** for easier usage

## 🤝 Support

If you encounter issues:
1. Check the troubleshooting section
2. Run `python ollama_setup.py` for model issues
3. Use `simple_extractor.py` as a fallback option
