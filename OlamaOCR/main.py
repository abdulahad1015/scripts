import os
import json
from pathlib import Path
import PyPDF2
import ollama
from typing import Dict, List, Any

class PDFTextExtractor:
    """Class to handle PDF text extraction and Ollama processing"""
    
    def __init__(self, cvs_folder: str = "CVs"):
        self.cvs_folder = Path(cvs_folder)
        self.extracted_data = {}
        
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from a PDF file"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {str(e)}")
            return ""
    
    def process_with_ollama(self, text: str, model: str = "llama3.2") -> Dict[str, Any]:
        """Process extracted text with Ollama to extract structured data"""
        prompt = f"""
        Please analyze the following resume/CV text and extract key information in JSON format.
        Extract the following fields if available:
        - name: Full name of the person
        - email: Email address
        - phone: Phone number
        - education: List of educational qualifications
        - experience: List of work experience
        - skills: List of technical and professional skills
        - summary: Brief professional summary
        
        Resume text:
        {text}
        
        Please respond with a valid JSON object containing the extracted information.
        """
        
        try:
            response = ollama.chat(model=model, messages=[
                {
                    'role': 'user',
                    'content': prompt,
                }
            ])
            
            # Try to parse the response as JSON
            response_text = response['message']['content']
            
            # Clean up the response to extract JSON
            if '```json' in response_text:
                json_start = response_text.find('```json') + 7
                json_end = response_text.find('```', json_start)
                json_text = response_text[json_start:json_end].strip()
            elif '{' in response_text and '}' in response_text:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                json_text = response_text[json_start:json_end]
            else:
                json_text = response_text
            
            try:
                return json.loads(json_text)
            except json.JSONDecodeError:
                # If JSON parsing fails, return a structured response
                return {
                    "raw_response": response_text,
                    "error": "Could not parse as JSON"
                }
                
        except Exception as e:
            print(f"Error processing with Ollama: {str(e)}")
            return {"error": str(e)}
    
    def process_all_pdfs(self, model: str) -> Dict[str, Any]:
        """Process all PDFs in the CVs folder"""
        if not self.cvs_folder.exists():
            print(f"CVs folder '{self.cvs_folder}' not found!")
            return {}
        
        pdf_files = list(self.cvs_folder.glob("*.pdf"))
        if not pdf_files:
            print(f"No PDF files found in '{self.cvs_folder}' folder!")
            return {}
        
        print(f"Found {len(pdf_files)} PDF files to process...")
        
        results = {}
        
        for pdf_file in pdf_files:
            print(f"\nProcessing: {pdf_file.name}")
            
            # Extract text from PDF
            print("  - Extracting text...")
            text = self.extract_text_from_pdf(pdf_file)
            
            if not text:
                print("  - No text extracted, skipping...")
                continue
            
            # Process with Ollama
            print("  - Processing with Ollama...")
            structured_data = self.process_with_ollama(text, model)
            
            results[pdf_file.name] = {
                "raw_text": text,
                "structured_data": structured_data,
                "file_path": str(pdf_file)
            }
            
            print(f"  - Completed processing {pdf_file.name}")
        
        return results
    
    def save_results(self, results: Dict[str, Any], output_file: str = "extracted_data.json"):
        """Save results to a JSON file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\nResults saved to: {output_file}")
        except Exception as e:
            print(f"Error saving results: {str(e)}")
    
    def print_summary(self, results: Dict[str, Any]):
        """Print a summary of extracted data"""
        print("\n" + "="*60)
        print("EXTRACTION SUMMARY")
        print("="*60)
        
        for filename, data in results.items():
            print(f"\nFile: {filename}")
            print("-" * 40)
            
            # Show basic text stats
            raw_text = data.get("raw_text", "")
            if raw_text:
                print(f"  Text length: {len(raw_text)} characters")
                print(f"  Lines: {len(raw_text.splitlines())}")
                # Show first 200 characters as preview
                preview = raw_text[:200].replace('\n', ' ').strip()
                print(f"  Preview: {preview}...")
            
            structured = data.get("structured_data", {})
            if "error" in structured:
                print(f"  Error: {structured['error']}")
                continue
            
            if "name" in structured:
                print(f"  Name: {structured['name']}")
            if "email" in structured:
                print(f"  Email: {structured['email']}")
            if "phone" in structured:
                print(f"  Phone: {structured['phone']}")
            if "skills" in structured:
                skills = structured['skills']
                if isinstance(skills, list):
                    # Handle case where skills might be a list of strings or dict objects
                    skill_strings = []
                    for skill in skills:
                        if isinstance(skill, str):
                            skill_strings.append(skill)
                        elif isinstance(skill, dict) and 'name' in skill:
                            skill_strings.append(skill['name'])
                        elif isinstance(skill, dict):
                            skill_strings.append(str(skill))
                        else:
                            skill_strings.append(str(skill))
                    print(f"  Skills: {', '.join(skill_strings[:5])}{'...' if len(skill_strings) > 5 else ''}")
                else:
                    print(f"  Skills: {skills}")

def main():
    """Main function to run the PDF text extraction and Ollama processing"""
    print("PDF Text Extractor with Ollama Processing")
    print("="*50)
    
    # Initialize the extractor
    extractor = PDFTextExtractor()
    
    # Check if Ollama is available
    try:
        models_response = ollama.list()
        available_models = [model.model for model in models_response.models]
        print(f"Available Ollama models: {available_models}")
        
        if not available_models:
            print("\nNo models found! Please install a model first.")
            print("Run: ollama pull llama3.2")
            return
        
        # Prefer llama3.2, otherwise use the first available model
        if "llama3.2:latest" in available_models:
            model_to_use = "llama3.2:latest"
        elif "llama3.2" in available_models:
            model_to_use = "llama3.2"
        elif any("llama3.2" in model for model in available_models):
            # Find the first llama3.2 variant
            model_to_use = next(model for model in available_models if "llama3.2" in model)
        else:
            model_to_use = available_models[0]
        
        print(f"Using model: {model_to_use}")
        
    except Exception as e:
        print(f"Error connecting to Ollama: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Make sure Ollama is installed: https://ollama.ai/")
        print("2. Start Ollama service: 'ollama serve'")
        print("3. Install a model: 'ollama pull llama3.2'")
        return
    
    # Process all PDFs
    results = extractor.process_all_pdfs(model=model_to_use)
    
    if results:
        # Save results
        extractor.save_results(results)
        
        # Print summary
        extractor.print_summary(results)
        
        print(f"\nProcessed {len(results)} files successfully!")
    else:
        print("No files were processed.")

if __name__ == "__main__":
    main()
