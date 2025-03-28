import customtkinter as ctk
from discord_webhook import DiscordWebhook, DiscordEmbed
import tkinter.messagebox as tkmb
from tkinter import filedialog

class WebhookMessenger:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.geometry("500x400")
        self.window.title("Discord Webhook Sender")
        self.image_path = None
        
        ctk.set_appearance_mode("dark")
        
        # Webhook URL input
        self.webhook_entry = ctk.CTkEntry(self.window, width=400, placeholder_text="Webhook URL")
        self.webhook_entry.pack(pady=10)
        
        # Title input
        self.title_entry = ctk.CTkEntry(self.window, width=400, placeholder_text="Enter Title")
        self.title_entry.pack(pady=10)
        
        # Message input
        self.message_text = ctk.CTkTextbox(self.window, width=400, height=150)
        self.message_text.pack(pady=10)
        
        # Image button
        self.image_button = ctk.CTkButton(self.window, text="Add Image", command=self.select_image)
        self.image_button.pack(pady=10)
        
        # Image label
        self.image_label = ctk.CTkLabel(self.window, text="No image selected")
        self.image_label.pack(pady=5)
        
        # Send button
        self.send_button = ctk.CTkButton(self.window, text="Send", command=self.send_webhook)
        self.send_button.pack(pady=10)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
        if self.image_path:
            self.image_label.configure(text="Image selected: " + self.image_path.split('/')[-1])

    def send_webhook(self):
        url = self.webhook_entry.get()
        title = self.title_entry.get()
        message = self.message_text.get("1.0", "end-1c")
        
        # Create webhook with main title as content
        webhook = DiscordWebhook(url=url, content=f"# {title}")
        
        # Create embed for message and image
        embed = DiscordEmbed(description=message, color=0x3498db)
        
        if self.image_path:
            # Set thumbnail instead of full image for smaller display
            embed.set_thumbnail(url="attachment://image.png")
            with open(self.image_path, "rb") as f:
                webhook.add_file(file=f.read(), filename='image.png')
        
        webhook.add_embed(embed)
        webhook.execute()
        
        tkmb.showinfo("Success", "Message sent!")
        self.message_text.delete("1.0", "end")
        self.title_entry.delete(0, "end")
        self.image_path = None
        self.image_label.configure(text="No image selected")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = WebhookMessenger()
    app.run()
