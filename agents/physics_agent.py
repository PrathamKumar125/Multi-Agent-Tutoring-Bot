from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from tools.physics_constants import PhysicsConstantsLookup
import re
from typing import Dict, Any
from config import OLLAMA_BASE_URL, MODEL_NAME

class PhysicsAgent:
    """Specialist agent for physics-related queries."""

    def __init__(self):
        self.llm = OllamaLLM(
            base_url=OLLAMA_BASE_URL,
            model=MODEL_NAME,
            temperature=0.1
        )
        self.constants_lookup = PhysicsConstantsLookup()

        self.prompt_template = PromptTemplate(
            input_variables=["query", "constants_info"],
            template="""You are a physics tutor. Answer the following physics question clearly and step-by-step.
Use fundamental physics principles and provide educational explanations.

{constants_info}

Question: {query}

Provide a clear, educational response that helps the student understand the physics concepts involved."""
        )

    def _find_relevant_constants(self, query: str) -> str:
        """Find and format relevant physics constants mentioned in the query."""
        query_lower = query.lower()
        constants_info = ""

        # Check for specific constant names or related keywords
        constant_keywords = {
            'speed of light': 'speed_of_light',
            'light speed': 'speed_of_light',
            'c': 'speed_of_light',
            'gravitational constant': 'gravitational_constant',
            'gravity constant': 'gravitational_constant',
            'g': 'gravitational_constant',
            'planck': 'planck_constant',
            'avogadro': 'avogadro_number',
            'boltzmann': 'boltzmann_constant',
            'elementary charge': 'elementary_charge',
            'electron mass': 'electron_mass',
            'proton mass': 'proton_mass',
        }

        found_constants = []
        for keyword, const_name in constant_keywords.items():
            if keyword in query_lower:
                constant_data = self.constants_lookup.get_constant(const_name)
                if constant_data:
                    formatted = self.constants_lookup.format_constant(const_name, constant_data)
                    found_constants.append(formatted)

        if found_constants:
            constants_info = "Relevant Physical Constants:\n" + "\n".join(f"• {const}" for const in found_constants) + "\n"

        return constants_info

    def process_query(self, query: str) -> str:
        """Process a physics query and return a comprehensive response."""
        try:
            # Find relevant constants
            constants_info = self._find_relevant_constants(query)

            # Generate response
            chain = self.prompt_template | self.llm
            response = chain.invoke({
                "query": query,
                "constants_info": constants_info
            })

            # Clean up the response - remove any <think> sections
            if "<think>" in response and "</think>" in response:
                think_start = response.find("<think>")
                think_end = response.find("</think>") + len("</think>")
                response = response[:think_start] + response[think_end:]

            return response

        except Exception as e:
            return f"I apologize, but I encountered an error while processing your physics question: {str(e)}"

    def can_handle_query(self, query: str) -> bool:
        """Determine if this agent can handle the given query."""
        physics_keywords = [
            'physics', 'force', 'energy', 'motion', 'velocity', 'acceleration',
            'newton', 'gravity', 'electromagnetic', 'quantum', 'thermodynamics',
            'mechanics', 'optics', 'waves', 'electricity', 'magnetism',
            'momentum', 'kinetic', 'potential', 'work', 'power', 'pressure',
            'temperature', 'heat', 'light', 'radiation', 'atomic', 'nuclear',
            'relativity', 'particle', 'field', 'circuit', 'resistance',
            'current', 'voltage', 'frequency', 'wavelength', 'mass', 'weight'
        ]

        query_lower = query.lower()
        return any(keyword in query_lower for keyword in physics_keywords)
