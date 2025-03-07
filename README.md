# Omnimorphism SDK

Omnimorphism SDK is an automated development toolkit that enables seamless conversion and integration of objects across different libraries and systems. The SDK dynamically inspects the data structures of your objects and uses an AI agent to generate conversion code at build time. This allows you to convert your custom objects into formats compatible with libraries such as Open3D, NumPy, trimesh, ROS, and more, or to integrate heterogeneous datasets with different schemas.

## Features

- **Dynamic Data Structure Parsing:**  
  Uses Python introspection to automatically extract attributes and types from your objects.

- **AI-Driven Code Generation:**  
  Leverages a LangChain Agent (with potential future migration to LangGraph) to generate Python conversion functions dynamically. These functions convert objects from one format (or library) to another based on detailed prompts.

- **Unified Conversion API:**  
  With a simple interface such as `Omnimorph(obj).to('targetlib')`, the SDK automatically generates (or loads cached) conversion functions to convert your objects.

- **Automatic Caching & Version Control:**  
  Generated conversion code is stored in the `generated/` directory and automatically committed to version control (e.g., Git), making it easy to review and maintain.

- **Integrated Unit Testing:**  
  During the build phase, unit tests are run to verify the correctness of generated conversion code, ensuring that all conversions meet your expected logic.


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

