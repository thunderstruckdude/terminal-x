import os
import requests

class LLMProvider:
    def __init__(self, provider, api_key):
        self.provider = provider
        self.api_key = api_key
        
    def generate_command(self, prompt):
        """Generate shell command from natural language prompt."""
        if self.provider == "claude":
            return self._claude_generate(prompt)
        elif self.provider == "gemini":
            return self._gemini_generate(prompt)
        elif self.provider == "gpt4o":
            return self._gpt4o_generate(prompt)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def _claude_generate(self, prompt):
        """Generate command using Claude API."""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            
            system_prompt = """
            You are TerminalX, a command-line assistant that translates natural language into shell commands.
            Your task is to convert user requests into correct shell commands.
            Respond ONLY with the shell command, nothing else.
            If the request cannot be converted to a valid shell command or is potentially harmful,
            respond with "COMMAND_ERROR: [reason]".
            """
            
            message = client.messages.create(
                model="claude-3-sonnet-20240229",
                system=system_prompt,
                max_tokens=300,
                messages=[
                    {"role": "user", "content": f"Convert this to a shell command: {prompt}"}
                ]
            )
            
            response = message.content[0].text
            
            # Check if response indicates an error
            if response.startswith("COMMAND_ERROR:"):
                return None, response
                
            return response, None
            
        except Exception as e:
            return None, f"Error with Claude API: {str(e)}"
    
    def _gemini_generate(self, prompt):
        """Generate command using Gemini API."""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            # Use Gemini 2.0 Flash model
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            system_prompt = """
            You are TerminalX, a command-line assistant that translates natural language into shell commands.
            Your task is to convert user requests into correct linux commands.
            Respond ONLY with the shell command, nothing else.
            If the request cannot be converted to a valid linux command or is potentially harmful,
            respond with "COMMAND_ERROR: [reason]".
            """
            
            # For Gemini, combine system prompt and user prompt
            full_prompt = f"{system_prompt}\n\nConvert this to a shell command: {prompt}"
            
            # Simple content generation without system role
            response = model.generate_content(full_prompt)
            
            result = response.text.strip()
            
            # Check if response indicates an error
            if result.startswith("COMMAND_ERROR:"):
                return None, result
                
            return result, None
            
        except Exception as e:
            return None, f"Error with Gemini API: {str(e)}"

    def _gpt4o_generate(self, prompt):
        """Generate command using OpenAI's GPT-4o API."""
        try:
            import openai
            
            # Configure the client with the API key
            client = openai.OpenAI(api_key=self.api_key)
            
            system_prompt = """
            You are TerminalX, a command-line assistant that translates natural language into shell commands.
            Your task is to convert user requests into correct shell commands.
            Respond ONLY with the shell command, nothing else.
            If the request cannot be converted to a valid shell command or is potentially harmful,
            respond with "COMMAND_ERROR: [reason]".
            """
            
            # Create a chat completion using GPT-4o
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Convert this to a shell command: {prompt}"}
                ],
                max_tokens=300,
                temperature=0.2  # Lower temperature for more precise command generation
            )
            
            result = response.choices[0].message.content.strip()
            
            # Check if response indicates an error
            if result.startswith("COMMAND_ERROR:"):
                return None, result
                
            return result, None
            
        except Exception as e:
            return None, f"Error with OpenAI API: {str(e)}"


def get_provider_choices():
    """Return available LLM providers."""

    return ["claude", "gemini", "gpt4o"]  