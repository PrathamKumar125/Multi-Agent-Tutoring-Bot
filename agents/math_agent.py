from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from tools.calculator import Calculator
import re
from typing import Dict, Any
from config import OLLAMA_BASE_URL, MODEL_NAME

class MathAgent:
    """Specialist agent for mathematics-related queries."""

    def __init__(self):
        self.llm = OllamaLLM(
            base_url=OLLAMA_BASE_URL,
            model=MODEL_NAME,
            temperature=0.1
        )
        self.calculator = Calculator()

        self.prompt_template = PromptTemplate(
            input_variables=["query"],
            template="""You are a mathematics tutor. Answer the following math question clearly and step-by-step.
If the question involves calculations, show your work.

Question: {query}

Provide a clear, educational response that helps the student understand the concept and solution process."""
        )

    def _extract_calculations(self, text: str) -> list:
        """Extract mathematical expressions that can be calculated."""
        # Look for expressions with numbers and operators
        patterns = [
            r'\b\d+(?:\.\d+)?\s*[+\-*/^]\s*\d+(?:\.\d+)?\b',
            r'\b\d+(?:\.\d+)?\s*\^\s*\d+(?:\.\d+)?\b',
            r'√\d+(?:\.\d+)?',
        ]

        calculations = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            calculations.extend(matches)

        return calculations

    def _perform_calculations(self, calculations: list) -> Dict[str, float]:
        """Perform the extracted calculations using the calculator tool."""
        results = {}

        for calc in calculations:
            try:
                result = self.calculator.evaluate_expression(calc)
                results[calc] = result
            except Exception as e:
                results[calc] = f"Error: {str(e)}"

        return results

    def process_query(self, query: str) -> str:
        """Process a math query and return a comprehensive response."""
        try:
            # Generate initial response
            chain = self.prompt_template | self.llm
            response = chain.invoke({"query": query})

            # Clean up the response - remove any <think> sections
            if "<think>" in response and "</think>" in response:
                think_start = response.find("<think>")
                think_end = response.find("</think>") + len("</think>")
                response = response[:think_start] + response[think_end:]

            # Extract and perform calculations
            calculations = self._extract_calculations(query)
            if calculations:
                calc_results = self._perform_calculations(calculations)

                # Append calculation results
                if calc_results:
                    response += "\n\n**Calculations:**\n"
                    for expr, result in calc_results.items():
                        response += f"• {expr} = {result}\n"

            return response

        except Exception as e:
            return f"I apologize, but I encountered an error while processing your math question: {str(e)}"

    def can_handle_query(self, query: str) -> bool:
        """Determine if this agent can handle the given query."""
        math_keywords = [
            'calculate', 'solve', 'equation', 'algebra', 'geometry', 'trigonometry',
            'calculus', 'derivative', 'integral', 'math', 'mathematics', 'number',
            'addition', 'subtraction', 'multiplication', 'division', 'fraction',
            'percentage', 'ratio', 'proportion', 'polynomial', 'quadratic',
            'linear', 'graph', 'function', 'variable', 'coefficient'
        ]

        query_lower = query.lower()
        return any(keyword in query_lower for keyword in math_keywords)
