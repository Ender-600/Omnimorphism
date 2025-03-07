# Omnimorphism SDK

Omnimorphism SDK is an automated development toolkit that enables seamless conversion and integration of objects across different libraries and systems.

## Features

Dynamic Data Structure Parsing:

AI-Driven Code Generation:

Unified Conversion & Method Generation API:

Automatic Caching & Version Control:

Automated Unit Testing:

Flexible Data Integration:

## Installation & Setup

1. **Clone the Project**

   ```bash
   git clone https://github.com/Ender-600/Omnimorphism.git
   cd omnimorphism-sdk
   ```

2. **Create and Activate a Virtual Environment**  
   (Ensure that you use a Python version compatible with your system architecture)

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On macOS/Linux
   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**  
   Create a `.env` file in the project root and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Additional Notes

- **AI Agent & LangChain:**  
  The SDK currently uses a LangChain Agent to generate conversion code. Although LangChain agents are supported, newer projects may consider using LangGraph for increased flexibility. Future releases may offer migration options.

- **Version Control:**  
  Generated conversion code is automatically committed to separate Git branches, which allows for manual review and easy version tracking.

