from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from agents.math_agent import MathAgent
from agents.physics_agent import PhysicsAgent
from typing import Optional
from config import OLLAMA_BASE_URL, MODEL_NAME
import logging
import traceback

class TutorAgent:
    """Main agent that orchestrates interactions and delegates to specialist agents."""

    def __init__(self):
        logging.info(f"TutorAgent: Initializing with model {MODEL_NAME} at {OLLAMA_BASE_URL}")
        try:
            self.llm = OllamaLLM(
                base_url=OLLAMA_BASE_URL,
                model=MODEL_NAME,
                temperature=0.3
            )
            logging.info("TutorAgent: LLM initialized successfully")

            # Initialize specialist agents
            logging.info("TutorAgent: Initializing Math Agent")
            self.math_agent = MathAgent()
            logging.info("TutorAgent: Initializing Physics Agent")
            self.physics_agent = PhysicsAgent()
            logging.info("TutorAgent: Specialist agents initialized")

            # Classification prompt for intent recognition
            self.classification_prompt = PromptTemplate(
                input_variables=["query"],
                template="""Classify the following student query into one of these categories:
- MATH: Mathematics, algebra, calculus, geometry, arithmetic, equations, numbers
- PHYSICS: Physics, forces, energy, motion, thermodynamics, electricity, mechanics
- GENERAL: General questions, greetings, or unclear topics

Query: {query}

Respond with only one word: MATH, PHYSICS, or GENERAL"""
            )

            # General response prompt
            self.general_prompt = PromptTemplate(
                input_variables=["query"],
                template="""You are a friendly tutor. Respond to the student's query helpfully.
If they're asking about topics you can help with, mention that you specialize in mathematics and physics.

Student: {query}

Provide a helpful and encouraging response."""
            )
            logging.info("TutorAgent: Prompts initialized")
        except Exception as e:
            error_details = traceback.format_exc()
            logging.error(f"TutorAgent: Error during initialization: {str(e)}")
            logging.error(f"TutorAgent: Traceback: {error_details}")
            raise

    def _classify_query(self, query: str) -> str:
        """Classify the query to determine which agent should handle it."""
        try:
            # First, check if specialist agents can handle it directly
            logging.info("TutorAgent: Checking if Math Agent can handle query")
            if self.math_agent.can_handle_query(query):
                logging.info("TutorAgent: Math Agent can handle query")
                return "MATH"

            logging.info("TutorAgent: Checking if Physics Agent can handle query")
            if self.physics_agent.can_handle_query(query):
                logging.info("TutorAgent: Physics Agent can handle query")
                return "PHYSICS"

            # Use LLM for classification if keyword matching is unclear
            logging.info("TutorAgent: Using LLM for classification")
            chain = self.classification_prompt | self.llm
            classification = chain.invoke({"query": query}).strip().upper()
            logging.info(f"TutorAgent: LLM classification result: {classification}")

            # Validate classification result
            if classification in ["MATH", "PHYSICS", "GENERAL"]:
                return classification
            else:
                logging.info(f"TutorAgent: Invalid classification '{classification}', defaulting to GENERAL")
                return "GENERAL"

        except Exception as e:
            error_details = traceback.format_exc()
            logging.error(f"TutorAgent: Error during classification: {str(e)}")
            logging.error(f"TutorAgent: Traceback: {error_details}")
            return "GENERAL"

    def process_query(self, query: str) -> str:
        """Process a student query by delegating to the appropriate agent."""
        if not query or not query.strip():
            return "Please ask me a question about mathematics or physics, and I'll be happy to help!"

        try:
            logging.info(f"TutorAgent: Processing query: '{query}'")

            # Classify the query
            logging.info("TutorAgent: Classifying query...")
            classification = self._classify_query(query)
            logging.info(f"TutorAgent: Query classified as: {classification}")

            # Delegate to appropriate agent
            if classification == "MATH":
                logging.info("TutorAgent: Delegating to Math Agent")
                response = self.math_agent.process_query(query)
                return f"**Mathematics Help:**\n\n{response}"

            elif classification == "PHYSICS":
                logging.info("TutorAgent: Delegating to Physics Agent")
                response = self.physics_agent.process_query(query)
                return f"**Physics Help:**\n\n{response}"

            else:  # GENERAL
                logging.info("TutorAgent: Handling as general query")
                chain = self.general_prompt | self.llm
                logging.info("TutorAgent: Invoking LLM for general response")
                response = chain.invoke({"query": query})
                logging.info("TutorAgent: LLM response received")
                return f"**General Response:**\n\n{response}"

        except Exception as e:
            error_details = traceback.format_exc()
            logging.error(f"TutorAgent: Error processing query: {str(e)}")
            logging.error(f"TutorAgent: Traceback: {error_details}")
            return f"I apologize, but I encountered an error while processing your question. Please try rephrasing your query or ask about a specific mathematics or physics topic. Error: {str(e)}"

    def get_capabilities(self) -> str:
        """Return information about the tutor's capabilities."""
        return """🎓 **Multi-Agent Tutoring Bot Capabilities:**

**Mathematics Agent** 🔢
- Algebra, calculus, geometry, trigonometry
- Equation solving and step-by-step solutions
- Built-in calculator for arithmetic operations
- Mathematical concept explanations

**Physics Agent** ⚡
- Classical mechanics, thermodynamics, electromagnetism
- Physics problem solving with relevant formulas
- Access to physical constants database
- Conceptual explanations with real-world applications

**How to use:**
- Ask specific questions like "What is Newton's second law?" or "Solve 2x + 5 = 11"
- I'll automatically route your question to the best specialist agent
- Get detailed, educational explanations tailored to your needs

Feel free to ask me anything about mathematics or physics!"""
