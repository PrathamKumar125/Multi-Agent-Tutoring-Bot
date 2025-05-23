import gradio as gr
from agents.tutor_agent import TutorAgent
import time
import logging
import traceback
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tutoring_bot.log"),
        logging.StreamHandler()
    ]
)

class TutoringBotApp:
    """Main application class for the Multi-Agent Tutoring Bot."""

    def __init__(self):
        self.tutor_agent = TutorAgent()
        self.conversation_history = []

    def chat_response(self, message, history):
        """Handle chat responses with conversation history."""
        if not message.strip():
            return history, ""

        # Process the query
        try:
            logging.info(f"Processing query: {message}")
            response = self.tutor_agent.process_query(message)
            logging.info(f"Query processed successfully. Response: {response[:100]}...")

            # Ensure response is a string
            if response is None:
                response = "I apologize, but I couldn't generate a response. Please try again."
                logging.warning("Response was None, using default message")

            # Add to history using the new messages format
            new_history = list(history)  # Create a copy to avoid modifying the original
            new_history.append({"role": "user", "content": message})
            new_history.append({"role": "assistant", "content": response})

            # Log the history for debugging
            logging.info(f"Updated history length: {len(new_history)}")
            if len(new_history) > 0:
                logging.info(f"Last history item: {new_history[-1]}")

            # Store in conversation history
            self.conversation_history.append({
                "user": message,
                "bot": response,
                "timestamp": time.time()
            })

            return new_history, ""

        except Exception as e:
            error_details = traceback.format_exc()
            logging.error(f"Error processing query: {str(e)}")
            logging.error(f"Traceback: {error_details}")

            error_response = f"I apologize, but I encountered an error. Please make sure Ollama is running and try again. Error: {str(e)}"

            new_history = list(history)  # Create a copy to avoid modifying the original
            new_history.append({"role": "user", "content": message})
            new_history.append({"role": "assistant", "content": error_response})

            return new_history, ""

    def show_capabilities(self):
        """Display bot capabilities."""
        return self.tutor_agent.get_capabilities()

    def clear_conversation(self):
        """Clear the conversation history."""
        self.conversation_history = []
        return []

    def create_interface(self):
        """Create and configure the Gradio interface."""
        with gr.Blocks(
            title="Multi-Agent Tutoring Bot",
            theme=gr.themes.Soft(),
            css="""
            .main-header {
                text-align: center;
                color: #2E8B57;
                margin-bottom: 20px;
            }
            .info-box {
                background-color: #f0f8ff;
                padding: 15px;
                border-radius: 10px;
                border: 1px solid #add8e6;
                margin: 10px 0;
            }
            """
        ) as demo:

            gr.Markdown(
                """
                # 🎓 Multi-Agent Tutoring Bot
                ### Powered by LangChain, Ollama, and Gradio

                Get help with **Mathematics** and **Physics** from specialized AI agents!
                """,
                elem_classes=["main-header"]
            )

            with gr.Row():
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(
                        height=500,
                        show_label=False,
                        avatar_images=[
                            "https://cdn-icons-png.flaticon.com/512/3135/3135810.png",  # Student icon
                            "https://cdn-icons-png.flaticon.com/512/4712/4712027.png"   # Robot icon
                        ],
                        type="messages",
                        render_markdown=True
                    )

                    msg = gr.Textbox(
                        placeholder="Ask me about mathematics or physics...",
                        label="Your Question",
                        lines=2
                    )

                    with gr.Row():
                        submit_btn = gr.Button("Send", variant="primary")
                        clear_btn = gr.Button("Clear Chat", variant="secondary")

                with gr.Column(scale=1):
                    gr.Markdown(
                        """
                        ### 📚 Quick Examples
                        **Mathematics:**
                        - "Solve the equation 2x + 5 = 11"
                        - "What is the derivative of x²?"
                        - "Calculate 15 × 23"

                        **Physics:**
                        - "What is Newton's second law?"
                        - "Explain kinetic energy"
                        - "What is the speed of light?"

                        ### ⚙️ System Info
                        - **Model:** Qwen3 0.6b via Ollama
                        - **Framework:** LangChain
                        - **Agents:** Math & Physics specialists
                        """,
                        elem_classes=["info-box"]
                    )

                    capabilities_btn = gr.Button("Show Full Capabilities")
                    capabilities_output = gr.Markdown(visible=False)

            # Event handlers
            def submit_message(message, history):
                logging.info(f"Submit message called with message: '{message}'")
                logging.info(f"Current history length: {len(history) if history else 0}")

                # Ensure message is not empty
                if not message or not message.strip():
                    logging.warning("Empty message submitted, ignoring")
                    return history, ""

                # Process the message and get updated history
                updated_history, _ = self.chat_response(message, history)
                logging.info(f"Updated history returned with length: {len(updated_history)}")

                return updated_history, ""

            def clear_chat():
                return self.clear_conversation()

            def toggle_capabilities():
                capabilities_text = self.show_capabilities()
                return gr.Markdown(capabilities_text, visible=True)

            # Wire up the events
            msg.submit(
                submit_message,
                inputs=[msg, chatbot],
                outputs=[chatbot, msg]
            )

            submit_btn.click(
                submit_message,
                inputs=[msg, chatbot],
                outputs=[chatbot, msg]
            )

            clear_btn.click(
                clear_chat,
                outputs=[chatbot]
            )

            capabilities_btn.click(
                toggle_capabilities,
                outputs=[capabilities_output]
            )

            # Welcome message - updated for new format
            demo.load(
                lambda: [{"role": "assistant", "content": "Hello! I'm your AI tutoring assistant. I can help you with mathematics and physics questions. What would you like to learn about today?"}],
                outputs=[chatbot]
            )

        return demo

def main():
    """Main function to run the application."""
    print("Starting Multi-Agent Tutoring Bot...")
    print("Make sure Ollama is running with qwen3:0.6b model")

    logging.info("Initializing Tutoring Bot application")

    try:
        app = TutoringBotApp()
        demo = app.create_interface()

        logging.info("Application initialized successfully")

        # Launch the app
        server_name = os.environ.get("SERVER_NAME", "127.0.0.1")
        server_port = int(os.environ.get("SERVER_PORT", "7860"))
        logging.info(f"Launching web interface on http://{server_name}:{server_port}")
        demo.launch(
            server_name="0.0.0.0", 
            server_port=7860,
            share=False,
            show_error=True,
            quiet=False,
            debug=True
        )
    except Exception as e:
        error_details = traceback.format_exc()
        logging.error(f"Failed to start application: {str(e)}")
        logging.error(f"Traceback: {error_details}")
        print(f"Error starting application: {str(e)}")
        print("Check tutoring_bot.log for details")

if __name__ == "__main__":
    main()
