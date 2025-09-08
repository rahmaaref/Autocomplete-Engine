import tkinter as tk
from tkinter import ttk
from trie import Trie
from dictionary import Dictionary

class AutoCompleteApp:
    def __init__(self, root, trie):
        self.trie = trie
        self.previous_text = ""
        
       
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a modern theme
        
        self.bg_color = "#f5f5f5"
        self.entry_bg = "#A7AFB3"
        self.listbox_bg = "#ffffff"
        self.listbox_sel = "#e1e1e1"
        self.accent_color = "#000000"
        self.text_color = "#333333"
        self.hint_color = "#666666"
        
   
        root.configure(bg=self.bg_color)
        
        # Create a main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a title label
        title_label = ttk.Label(
            main_frame, 
            text="AutoComplete Engine", 
            font=('Arial', 16, 'bold'),
            foreground=self.accent_color
        )
        title_label.pack(pady=(0, 15))
        
        # Create the text entry field 
        self.entry = ttk.Entry(
            main_frame, 
            width=40, 
            font=('Arial', 12)
        )
        self.entry.pack(pady=10, fill=tk.X)
        self.entry.bind("<KeyRelease>", self.on_key)
        self.entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.entry.bind("<FocusOut>", self.on_entry_focus_out)
        
        # Set placeholder text
        self.placeholder_text = "Continue typing"
        self.entry.insert(0, self.placeholder_text)
        self.entry.configure(foreground=self.hint_color)
        
        # Create a frame for the suggestions listbox
        listbox_frame = ttk.Frame(main_frame, relief=tk.SUNKEN, borderwidth=1)
        listbox_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # Create the suggestions listbox
        self.listbox = tk.Listbox(
            listbox_frame, 
            width=40, 
            height=8, 
            font=('Arial', 11),
            bg=self.listbox_bg,
            relief=tk.FLAT,
            highlightthickness=0,
            selectbackground=self.listbox_sel,
            selectforeground=self.text_color
        )
        
        # Add scrollbar to listbox
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1, pady=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind listbox selection to entry field
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        
        # Add instructions label
        self.label = ttk.Label(
            main_frame, 
            font=('Arial', 10), 
            foreground=self.hint_color,
            wraplength=350
        )
        self.label.pack(pady=10)
        
        # Add a status bar at the bottom
        self.status = ttk.Label(
            root, 
            text="Ready", 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            font=('Arial', 9),
            foreground=self.hint_color
        )
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
    
    def on_entry_focus_in(self, event):
        """Handle focus in event to remove placeholder text"""
        if self.entry.get() == self.placeholder_text:
            self.entry.delete(0, tk.END)
            self.entry.configure(foreground=self.text_color)
    
    def on_entry_focus_out(self, event):
        """Handle focus out event to add placeholder text if empty"""
        if not self.entry.get():
            self.entry.insert(0, self.placeholder_text)
            self.entry.configure(foreground=self.hint_color)
    
    def on_select(self, event):
        """Handle selection from the listbox"""
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            value = self.listbox.get(index)
            
            # Get current cursor position and word boundaries
            current_text = self.entry.get()
            cursor_pos = self.entry.index(tk.INSERT)
            
            # Find word boundaries
            start = cursor_pos
            while start > 0 and current_text[start-1].isalpha():
                start -= 1
            
            # Replace the current word with the selected suggestion
            self.entry.delete(start, tk.END)
            self.entry.insert(start, value)
            
            # Clear the suggestions
            self.listbox.delete(0, tk.END)
       
    
    def is_new_word_starting(self, current_text):
        """Check if a new word is starting based on the current and previous text."""
        if not current_text or current_text == self.placeholder_text:
            return False
        
        # If we just started typing (no previous text)
        if not self.previous_text or self.previous_text == self.placeholder_text:
            return len(current_text) == 1 and current_text.isalpha()
        
        # If current text is shorter, user deleted something
        if len(current_text) < len(self.previous_text):
            return False
        
        # Get the last character that was added
        if len(current_text) > len(self.previous_text):
            last_char = current_text[-1]
            
            # New word starts after space, punctuation, or at the beginning
            if len(current_text) == 1:
                return last_char.isalpha()
            
            # Check if we just started a new word after a space or punctuation
            prev_char = current_text[-2] if len(current_text) >= 2 else ""
            return last_char.isalpha() and (prev_char.isspace() or not prev_char.isalpha())
        
        return False
    
    def get_current_word_and_position(self, text):
        """Get the current word being typed and its start position."""
        if text == self.placeholder_text:
            return "", 0
            
        cursor_pos = self.entry.index(tk.INSERT)
        
        # Find word boundaries
        start = cursor_pos
        while start > 0 and text[start-1].isalpha():
            start -= 1
        
        end = cursor_pos
        while end < len(text) and text[end].isalpha():
            end += 1
        
        current_word = text[start:end]
        return current_word.lower(), start
    
    def on_key(self, event):        
        current_text = self.entry.get()
        
        # Ignore if we're showing placeholder text
        if current_text == self.placeholder_text:
            self.listbox.delete(0, tk.END)
            self.label.config(text="Start typing")
            self.previous_text = current_text
            return
        
        # Always clear suggestions first
        self.listbox.delete(0, tk.END)
        
        # Check if we should show suggestions
        should_show_suggestions = False
        
        # Show suggestions if a new word is starting
        if self.is_new_word_starting(current_text):
            should_show_suggestions = True
        
        # Show suggestions if we're continuing to type in the current word
        elif current_text:
            current_word, _ = self.get_current_word_and_position(current_text)
            if current_word and len(current_word) > 0:
                should_show_suggestions = True
        
        if should_show_suggestions:
            current_word, _ = self.get_current_word_and_position(current_text)
            if current_word:
                try:
                    suggestions = self.trie.starts_with(current_word, limit=8)  # Show more suggestions
                    if suggestions:
                        for word, freq in suggestions:
                            self.listbox.insert(tk.END, word)
                        self.status.config(text=f"Showing {len(suggestions)} suggestions")
                    else:
                        self.listbox.insert(tk.END, "No suggestions found")
                        self.label.config(text=f"No suggestions found for '{current_word}'")
                        self.status.config(text="No suggestions available")
                except Exception as e:
                    self.listbox.insert(tk.END, f"Error: {str(e)}")
                    self.label.config(text="Error getting suggestions")
                    self.status.config(text="Error occurred")
        else:
            self.label.config(text="Start typing")
            self.status.config(text="Ready")
        
        # Update previous text for next comparison
        self.previous_text = current_text

def main():
    # Create the main window
    root = tk.Tk()
    root.title("AutoComplete Engine")
    root.geometry("500x400")
    root.resizable(True, True)
    root.configure(bg="#f5f5f5")
    
    # Center the window on screen
    root.eval('tk::PlaceWindow . center')
    
    try:
        # Load dictionary and create trie
        print("Loading dictionary...")
        d = Dictionary("data/unigram_freq.csv")
        
        print("Building trie...")
        trie = Trie()
        for word, freq in d.word_freq.items():
            trie.insert(word, freq)
        
        print("Starting GUI...")
        
        # Create the app
        app = AutoCompleteApp(root, trie)
        
        # Start the GUI event loop
        root.mainloop()
        
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Make sure 'trie.py' and 'dictionary.py' files exist")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()