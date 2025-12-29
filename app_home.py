"""
Remade Tkinter app with proper GPU usage and memory-safety.

Notes:
- Set MODEL_PATH and OLLAMA_MODEL as needed.
- If your Ollama install is CPU-only, chat inference will still run on CPU.
- This script ensures the Qwen model (Vision2Seq) is moved to GPU and inputs
  are moved to the same device before calling generate().
"""

import os
import json
import time
import threading
import subprocess
import gc
from concurrent.futures import ThreadPoolExecutor

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

import torch
from transformers import AutoProcessor, AutoModelForVision2Seq

# Optional: if you use customtkinter it's kept; fallback to normal tkinter if missing
try:
    import customtkinter as ctk
except Exception:
    ctk = None

# ==================== CONFIG ====================
MODEL_PATH = r"K:\Code\Project\Advanced_intelligent assistant\A_I_S_H_A\Qwen"
MEMORY_FILE = "chat_memory.json"
OLLAMA_MODEL = "gemma2:9b"

# Behavior tuning
MAX_CHAT_SAVE_BATCH = 5            # Save after this many chat changes
MAX_CHAT_MESSAGES = 200            # Keep only this many messages in memory
TEXT_TRUNCATE_THRESHOLD_LINES = 5000
TEXT_TRUNCATE_REMOVE_LINES = 1000
THREAD_POOL_SIZE = 2

# detect device
USE_CUDA = torch.cuda.is_available()
device = torch.device("cuda" if USE_CUDA else "cpu")

# Force CUDA context initialization on main thread (helps threads use CUDA reliably)
if USE_CUDA:
    try:
        # Accessing current_device initializes CUDA context
        _ = torch.cuda.current_device()
    except Exception:
        # best-effort: ignore initialization errors here; runtime errors will surface later
        pass

# Lazy-loaded model references and synchronization
processor = None
model = None
_model_lock = threading.Lock()
_model_loading = False

# Executor for background tasks (image inference, chat calls)
executor = ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE)

# ----------------- Helpers -----------------
def _log(msg: str):
    # Simple print wrapper; replace with a real logger if desired
    print(msg)

def _move_tensors_to_device(batch: dict, dev: torch.device):
    """
    Move all torch tensors in a nested dict to device.
    The processor returns dict[str, Tensor] (possibly)
    """
    moved = {}
    for k, v in batch.items():
        if isinstance(v, torch.Tensor):
            moved[k] = v.to(dev, non_blocking=True)
        elif isinstance(v, list):
            # sometimes processor returns lists (shouldn't happen for return_tensors="pt")
            try:
                # attempt to stack if tensors
                if v and isinstance(v[0], torch.Tensor):
                    moved[k] = torch.stack(v).to(dev, non_blocking=True)
                else:
                    moved[k] = v
            except Exception:
                moved[k] = v
        else:
            moved[k] = v
    return moved

def _clean_tensors(*objs):
    """
    Delete and collect garbage for tensors or large objects.
    """
    for o in objs:
        try:
            del o
        except Exception:
            pass
    gc.collect()
    if USE_CUDA:
        try:
            torch.cuda.empty_cache()
        except Exception:
            pass

# ----------------- Model loading -----------------
def load_qwen_if_needed(force_reload: bool = False) -> bool:
    """
    Lazy load the Qwen Vision2Seq processor + model.
    If CUDA is available, model will be moved to GPU (float16).
    Loads with low_cpu_mem_usage flag to reduce startup RAM usage.
    Thread-safe.
    """
    global processor, model, _model_loading

    with _model_lock:
        if not force_reload and processor is not None and model is not None:
            return True
        if _model_loading:
            # wait for other thread to finish
            while _model_loading:
                time.sleep(0.05)
            return processor is not None and model is not None
        _model_loading = True

    try:
        _log("🔄 Loading Qwen-VL model (lazy load)...")
        # Load processor (lightweight)
        proc = AutoProcessor.from_pretrained(MODEL_PATH)

        # Load model with low CPU memory usage; then move to device explicitly.
        dtype = torch.float16 if USE_CUDA else torch.float32

        # Using low_cpu_mem_usage can drastically reduce RAM at load time.
        m = AutoModelForVision2Seq.from_pretrained(
            MODEL_PATH,
            torch_dtype=dtype,
            low_cpu_mem_usage=True,
        )

        # Move model to device (explicit)
        if USE_CUDA:
            try:
                m.to(device)
                # optionally enable eval-mode and gradient disabled
                m.eval()
            except Exception as e:
                _log(f"⚠️ Warning: Failed to move model to CUDA cleanly: {e}")
                # continue with CPU model if move fails
        else:
            m.to(device)
            m.eval()

        with _model_lock:
            processor = proc
            model = m

        _log("✅ Qwen model loaded successfully!")
        return True

    except Exception as e:
        _log(f"Failed to load Qwen: {e}")
        with _model_lock:
            processor = None
            model = None
        return False

    finally:
        with _model_lock:
            _model_loading = False

# ----------------- Ollama GPU check (best-effort) -----------------
def ollama_has_gpu() -> bool:
    """
    Best-effort check to detect if ollama is configured for GPU.
    This calls `ollama list` and inspects output. If ollama is missing or the output
    is unexpected, return False (conservative).
    """
    try:
        p = subprocess.run(["ollama", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=4)
        out = p.stdout.lower()
        # Heuristics: if 'gpu' or 'cuda' strings appear in output for the target model
        return "gpu" in out or "cuda" in out
    except Exception:
        return False

# ==================== MAIN APP ====================
class app_Home(Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="white")
        self.controller = controller

        # runtime state
        self.last_extracted_text = ""
        self.chat_memory = self.load_memory()
        self._unsaved_changes = 0

        # limited thumbnails
        self._thumbnail_refs = []

        # build UI
        self._build_ui()
        self.display_old_chats()

        # quick ollama GPU status
        self.ollama_gpu = ollama_has_gpu()
        if USE_CUDA:
            _log(f"CUDA available: True  (device: {torch.cuda.get_device_name(0)})")
        else:
            _log("CUDA available: False")
        _log(f"Ollama GPU available (best-effort): {self.ollama_gpu}")

    # ---------------- UI construction ----------------
    def _build_ui(self):
        # left menu
        frame1 = Label(self, bd=1, relief=RIDGE, bg="gray91")
        frame1.place(x=0, y=0, width=300, height=700)

        Label(frame1, text="Chats", font=("Comic Sans MS", 14, "bold"), bg="gray91", fg="black").place(x=0, y=200)

        Button(frame1, text="📖 New chat", font=("Arial Rounded MT Bold", 12),
               bg="gray91", fg="black", bd=0, command=self.clear_memory).place(x=0, y=110, width=298, height=30)
        Button(frame1, text="📲 Share", font=("Arial Rounded MT Bold", 12),
               bg="gray91", fg="black", bd=0).place(x=0, y=170, width=298, height=30)

        # slider and nav
        self.slider_expend = False
        self.slider_frame = Frame(self, bg="gray91", width=298, height=100)
        self.slider_frame.place(x=0, y=0)
        if ctk:
            self.menu_button = ctk.CTkButton(self.slider_frame, text="☰", width=30, height=30,
                                             fg_color="transparent", text_color="black",
                                             font=("Arial", 22), command=self.toggle_slider)
        else:
            self.menu_button = Button(self.slider_frame, text="☰", command=self.toggle_slider)
        self.menu_button.place(anchor="nw", x=10, y=10)

        self.settings_button = Button(self.slider_frame, text="⚙️ Settings",
                                      font=("Arial Rounded MT Bold", 12), bg="gray91", fg="black", bd=0)
        self.logout_button = Button(self.slider_frame, text="🚪 Log Out",
                                    font=("Arial Rounded MT Bold", 12), bg="gray91", fg="black", bd=0)
        self.nav_buttons = [self.settings_button, self.logout_button]

        # chat display
        frame2 = Frame(self, bg="white")
        frame2.place(x=390, y=0, width=800, height=560)

        self.show_text_field = Text(frame2, wrap='word', font=("Helvetica", 12), bg="white", fg="black",
                                    bd=0, height=15, state='disabled')
        self.show_text_field.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        if ctk:
            scrollbar_output = ctk.CTkScrollbar(frame2, command=self.show_text_field.yview, fg_color="transparent")
        else:
            scrollbar_output = Scrollbar(frame2, command=self.show_text_field.yview)
        scrollbar_output.pack(side='right', fill='y')
        self.show_text_field.configure(yscrollcommand=scrollbar_output.set)

        # input area
        frame3 = Frame(self, bd=2, bg="white")
        frame3.place(x=460, y=550, width=600, height=80)

        if ctk:
            self.image_button = ctk.CTkButton(frame3, fg_color="white", text="+", font=("Arial", 40),
                                             text_color="gray63", hover_color="gray91", corner_radius=30,
                                             command=self.insert_image)
            self.input_text_field = ctk.CTkTextbox(frame3, wrap='word', font=("Helvetica", 15),
                                                   border_width=2, border_color="gray90",
                                                   text_color="black", fg_color="white", corner_radius=15)
        else:
            self.image_button = Button(frame3, text="+", font=("Arial", 40), command=self.insert_image)
            self.input_text_field = Text(frame3, wrap='word', font=("Helvetica", 15), height=2)

        self.image_button.pack(side="left", padx=(5, 0))
        self.input_text_field.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        # event bindings (for both Text and CTkTextbox)
        try:
            self.input_text_field.bind("<KeyRelease>", self.input_auto_resize)
            self.input_text_field.bind("<Return>", self.handle_return)
        except Exception:
            pass

    # ---------------- MEMORY: load / save / trim ----------------
    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data[-MAX_CHAT_MESSAGES:]
            except Exception:
                return []
        return []

    def _schedule_save(self):
        self._unsaved_changes += 1
        if self._unsaved_changes >= MAX_CHAT_SAVE_BATCH:
            self.save_memory()
            self._unsaved_changes = 0

    def save_memory(self):
        try:
            self.chat_memory = self.chat_memory[-MAX_CHAT_MESSAGES:]
            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.chat_memory, f, indent=2, ensure_ascii=False)
        except Exception as e:
            _log(f"Failed to save memory: {e}")

    def clear_memory(self):
        self.chat_memory = []
        self.save_memory()
        self._append_to_chat_widget("🧹 New chat started.\n\n")

    def display_old_chats(self):
        if self.chat_memory:
            self._append_to_chat_widget("💾 Restored previous chat:\n\n")
            for msg in self.chat_memory[-10:]:
                role, text = msg.get("role"), msg.get("text")
                if role == "user":
                    self._append_to_chat_widget(f"🧑 You: {text}\n\n")
                else:
                    self._append_to_chat_widget(f"🤖 Gemma: {text}\n\n")

    # ---------------- UI helpers ----------------
    def toggle_slider(self):
        if self.slider_expend:
            for btn in self.nav_buttons:
                btn.place_forget()
            self.slider_expend = False
        else:
            self.settings_button.place(x=0, y=40, width=298, height=30)
            self.logout_button.place(x=0, y=70, width=298, height=30)
            self.slider_expend = True

    def input_auto_resize(self, event=None):
        try:
            line_count = int(self.input_text_field.index('end-1c').split('.')[0])
            new_height = min(max(line_count, 1), 6)
            self.input_text_field.configure(height=new_height)
        except Exception:
            # unsupported control, ignore
            pass

    def handle_return(self, event=None):
        # allow shift+enter for newline
        if event is not None and (event.state & 0x0001):
            return None
        return self.send_message(event)

    # central helper to append to Text widget safely and truncate if needed
    def _append_to_chat_widget(self, text: str):
        # Ensure modifications happen on main thread
        def _do():
            self.show_text_field.config(state='normal')
            self.show_text_field.insert(END, text)
            self.show_text_field.config(state='disabled')
            self.show_text_field.see(END)

            total_lines = int(self.show_text_field.index('end-1c').split('.')[0])
            if total_lines > TEXT_TRUNCATE_THRESHOLD_LINES:
                self.show_text_field.config(state='normal')
                self.show_text_field.delete('1.0', f'{TEXT_TRUNCATE_REMOVE_LINES}.0')
                self.show_text_field.config(state='disabled')

        try:
            # if called from worker thread, use after
            self.show_text_field.after(0, _do)
        except Exception:
            _do()

    # ---------------- Chat (user input) ----------------
    def send_message(self, event=None):
        try:
            msg = self.input_text_field.get("1.0", "end-1c").strip()
        except Exception:
            # for CTkTextbox
            msg = self.input_text_field.get("0.0", "end-1c").strip()

        if not msg:
            return "break"

        self._append_to_chat_widget(f"🧑 You: {msg}\n\n")
        try:
            self.input_text_field.delete("1.0", END)
        except Exception:
            try:
                self.input_text_field.delete("0.0", END)
            except Exception:
                pass
        self.input_auto_resize()

        self.chat_memory.append({"role": "user", "text": msg})
        self._schedule_save()

        # Use executor to limit concurrent workers
        executor.submit(self.ask_llama_chat, msg)
        return "break"

    def ask_llama_chat(self, user_message: str):
        context = self.last_extracted_text.strip()
        if context:
            full_message = f"The following text was extracted from an image:\n{context}\n\nUser says:\n{user_message}"
        else:
            full_message = user_message

        cmd = ["ollama", "run", OLLAMA_MODEL, full_message]

        # Show initial label
        self._append_to_chat_widget("🤖 gemma2:9b: ")

        try:
            # Redirect stderr to DEVNULL to avoid spinner escape codes
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                encoding="utf-8",
                bufsize=1,
            )

            if process.stdout is not None:
                for line in iter(process.stdout.readline, ""):
                    if not line:
                        break
                    if line.strip():
                        # write chunk to UI
                        self._append_to_chat_widget(line)
                process.stdout.close()

            process.wait(timeout=None)
            self._append_to_chat_widget("\n\n")

        except Exception as e:
            self._append_to_chat_widget(f"⚠️ Error running Gemma: {e}\n")

    # ---------------- Image upload & Qwen inference ----------------
    def insert_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp")])
        if not file_path:
            return

        try:
            img = Image.open(file_path).convert("RGB")
        except Exception as e:
            self._append_to_chat_widget(f"⚠️ Failed to open image: {e}\n")
            return

        try:
            thumb = img.copy()
            thumb.thumbnail((350, 350))
            photo = ImageTk.PhotoImage(thumb)

            self._thumbnail_refs.append(photo)
            if len(self._thumbnail_refs) > 10:
                self._thumbnail_refs.pop(0)

            self.show_text_field.config(state='normal')
            image_label = Label(self.show_text_field, image=photo, bg="white")
            image_label.image = photo
            self.show_text_field.window_create(END, window=image_label)
            self.show_text_field.insert(END, "\n")
            self.show_text_field.config(state='disabled')

            # show status label
            self.result_label = Label(self.show_text_field, text="🤖 AI: Reading image...", font=("Helvetica", 13),
                                      bg="white", fg="black", wraplength=600)
            self.show_text_field.config(state='normal')
            self.show_text_field.window_create(END, window=self.result_label)
            self.show_text_field.insert(END, "\n\n")
            self.show_text_field.config(state='disabled')

        except Exception as e:
            self._append_to_chat_widget(f"⚠️ Failed to display thumbnail: {e}\n")
            try:
                img.close()
            except Exception:
                pass
            return
        finally:
            try:
                thumb.close()
            except Exception:
                pass

        # Run inference in executor
        # Pass file_path (less memory than passing the entire image)
        executor.submit(self.run_qwen_inference, file_path)

        # close the original image (we reopened it in worker)
        try:
            img.close()
        except Exception:
            pass

    def run_qwen_inference(self, file_path: str):
        ok = load_qwen_if_needed()
        if not ok:
            # inform user on main thread
            self.show_text_field.after(0, lambda: self.result_label.config(text="❌ Failed to load Qwen model."))
            return

        # Open image inside worker (so main thread memory stays small)
        try:
            with Image.open(file_path) as pil_img:
                pil_img = pil_img.convert("RGB")

                # Build message payload expected by Qwen processor
                messages = [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Read all visible text in this image."},
                        {"type": "image", "image": pil_img},
                    ],
                }]

                # Prepare prompt & tensors (processor returns dict of tensors)
                # We call processor on the worker thread; tensors are created on CPU then moved to device.
                text_prompt = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                inputs = processor(text=[text_prompt], images=[pil_img], return_tensors="pt")

                # Move all tensor inputs to device explicitly
                inputs = _move_tensors_to_device(inputs, device)

                # Generate (ensure model and inputs are on same device)
                with torch.no_grad():
                    # Ensure model is in eval()
                    with _model_lock:
                        m = model
                    # generation
                    output_ids = m.generate(**inputs, max_new_tokens=256)

                    # Move output_ids to CPU before decoding if needed
                    if output_ids.device != torch.device("cpu"):
                        output_ids = output_ids.cpu()

                    result = processor.batch_decode(output_ids, skip_special_tokens=True)[0]

                # cleanup large tensors
                _clean_tensors(inputs, output_ids)

        except Exception as e:
            result = f"⚠️ Qwen error: {e}"
            _log(result)

        # Update UI on main thread and record memory
        def _update_ui():
            self.last_extracted_text = result
            try:
                self.result_label.config(text=f"🧠 Qwen Result: {result}")
            except Exception:
                # fallback: append to chat
                self._append_to_chat_widget(f"🧠 Qwen Result: {result}\n\n")
            self.chat_memory.append({"role": "assistant", "text": f"(Qwen OCR): {result}"})
            self._schedule_save()

        try:
            self.show_text_field.after(0, _update_ui)
        except Exception:
            _update_ui()

