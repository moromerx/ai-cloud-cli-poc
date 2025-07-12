`ai-cloud-cli` is an intelligent command-line interface that lets you interact with your cloud environment using natural language. It understands your intent and executes AWS operations seamlessly through conversational commands.

## 🚀 Setup

### Prerequisites

- Python 3.8 or higher
- API key for your preferred AI provider (Currently supports OpenAI, Groq, and Ollama.)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/moromerx/ai-cloud-cli-poc.git
   cd ai-cloud-cli-poc
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **AWS Credentials**

   Ensure your AWS credentials are properly configured:

   ```bash
   aws configure
   ```

   Or set environment variables in your `.env` file.

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run**
   ```bash
   python main.py
   ```

### Example Interactions

```
ai-cloud-cli-poc> Show me all my EC2 instances
🤖 I'll check your EC2 instances for you...

ai-cloud-cli-poc> Create a new S3 bucket called my-project-assets
🤖 I'll create an S3 bucket named 'my-project-assets' for you...

ai-cloud-cli-poc> What's the status of my RDS databases?
🤖 Let me check the status of your RDS instances...
```

### Provider and Model Switching

**Supported Providers:** Currently supports OpenAI, Groq, and Ollama.

Switch between different AI providers and models:

```bash
--provider openai  
--provider groq    
--model gpt-4  
--model llama-3.3-70b-versatile
```
