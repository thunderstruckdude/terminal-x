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
            model = genai.GenerativeModel('gemini-pro')
            
            system_prompt = """
            You are TerminalX, a command-line assistant that translates natural language into shell commands.
            Your task is to convert user requests into correct shell commands.
            Respond ONLY with the shell command, nothing else.
            If the request cannot be converted to a valid shell command or is potentially harmful,
            respond with "COMMAND_ERROR: [reason]".
            """
            
            response = model.generate_content([
                system_prompt,
                f"Convert this to a shell command: {prompt}"
            ])
            
            result = response.text.strip()
            
            # Check if response indicates an error
            if result.startswith("COMMAND_ERROR:"):
                return None, result
                
            return result, None
            
        except Exception as e:
            return None, f"Error with Gemini API: {str(e)}"


def get_provider_choices():
    """Return available LLM providers."""
    return ["claude", "gemini"]