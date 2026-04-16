import gradio as gr
from groq import Groq
import os

# Initialize Mentor
class AIMentor:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.model = "llama-3.3-70b-versatile" 

    def generate_response(self, topic, level, options):
        if not self.api_key:
            return "### ❌ Error: GROQ_API_KEY not found in Secrets."
        if not topic:
            return "### Please enter a topic."
        
        options_str = ", ".join(options)
        system_prompt = f"You are an expert AI Mentor teaching {topic} at {level} level. Focus on: {options_str}."
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompt},
                          {"role": "user", "content": f"Teach me about {topic}."}],
                model=self.model,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"**Error:** {str(e)}"

mentor = AIMentor()
# Simple UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 AI Mentor")
    topic_in = gr.Textbox(label="Topic")
    level_in = gr.Dropdown(choices=["Beginner", "Intermediate", "Advanced"], label="Level")
    opts_in = gr.CheckboxGroup(choices=["Theory", "Problems", "Industry Practices"], label="Focus")
    submit = gr.Button("Teach Me!")
    output = gr.Markdown("Results will appear here.")
    submit.click(fn=mentor.generate_response, inputs=[topic_in, level_in, opts_in], outputs=output)

demo.launch()