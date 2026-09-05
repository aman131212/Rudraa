from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.animation import Animation
from openai import OpenAI
import threading
import math
import random


# =========================================================
# BASIC SETTINGS
# =========================================================

Window.softinput_mode = "resize"

BG = (0.018, 0.012, 0.045, 1)
WHITE = (0.94, 0.94, 0.98, 1)
MUTED = (0.52, 0.50, 0.62, 1)

VIOLET = (0.58, 0.27, 0.98, 1)
CYAN = (0.18, 0.78, 0.96, 1)
ROSE = (0.96, 0.30, 0.63, 1)
GOLD = (0.95, 0.67, 0.28, 1)

PANEL = (0.065, 0.038, 0.125, 0.96)
USER_PANEL = (0.14, 0.055, 0.22, 0.98)
AI_PANEL = (0.045, 0.055, 0.12, 0.98)


# =========================================================
# GLASS PANEL
# =========================================================

class GlassPanel(BoxLayout):

    def __init__(self, bg=PANEL, **kwargs):
        super().__init__(**kwargs)

        self.bg_color = bg

        with self.canvas.before:
            Color(*self.bg_color)

            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(18)]
            )

            Color(
                CYAN[0],
                CYAN[1],
                CYAN[2],
                0.10
            )

            self.line = Line(
                rounded_rectangle=(
                    self.x,
                    self.y,
                    self.width,
                    self.height,
                    dp(18)
                ),
                width=0.7
            )

        self.bind(
            pos=self.update_canvas,
            size=self.update_canvas
        )

    def update_canvas(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

        self.line.rounded_rectangle = (
            self.x,
            self.y,
            self.width,
            self.height,
            dp(18)
        )


# =========================================================
# ANIMATED BACKGROUND
# =========================================================

class AnimatedBackground(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.time = 0

        with self.canvas.before:

            Color(*BG)

            self.background = RoundedRectangle(
                pos=self.pos,
                size=self.size
            )

            # Large soft aura
            Color(
                VIOLET[0],
                VIOLET[1],
                VIOLET[2],
                0.13
            )

            self.aura1 = Ellipse()

            # Cyan atmosphere
            Color(
                CYAN[0],
                CYAN[1],
                CYAN[2],
                0.07
            )

            self.aura2 = Ellipse()

            # Orbit
            Color(
                VIOLET[0],
                VIOLET[1],
                VIOLET[2],
                0.16
            )

            self.orbit = Line(
                ellipse=(
                    dp(-90),
                    dp(230),
                    dp(470),
                    dp(260)
                ),
                width=1
            )

            # Decorative particles
            self.particles = []

            for i in range(12):

                Color(
                    CYAN[0],
                    CYAN[1],
                    CYAN[2],
                    random.uniform(0.12, 0.30)
                )

                dot = Ellipse(
                    size=(dp(2), dp(2))
                )

                self.particles.append({
                    "shape": dot,
                    "x": random.random(),
                    "y": random.random(),
                    "phase": random.random() * 6.28
                })

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

        # Lightweight animation
        Clock.schedule_interval(
            self.animate,
            1 / 20.0
        )

    def update_background(self, *args):

        self.background.pos = self.pos
        self.background.size = self.size

        self.aura1.pos = (
            self.width * 0.40,
            self.height * 0.60
        )

        self.aura1.size = (
            dp(260),
            dp(260)
        )

        self.aura2.pos = (
            self.width * 0.02,
            self.height * 0.15
        )

        self.aura2.size = (
            dp(220),
            dp(220)
        )

    def animate(self, dt):

        self.time += dt

        pulse = (
            math.sin(self.time * 0.7) + 1
        ) / 2

        size1 = dp(245 + pulse * 35)

        self.aura1.size = (
            size1,
            size1
        )

        self.aura1.pos = (
            self.width * 0.40,
            self.height * 0.60
        )

        # Slowly moving particles
        for p in self.particles:

            x = (
                p["x"] * self.width
                + math.sin(
                    self.time * 0.25 +
                    p["phase"]
                ) * dp(5)
            )

            y = (
                p["y"] * self.height
                + math.cos(
                    self.time * 0.20 +
                    p["phase"]
                ) * dp(5)
            )

            p["shape"].pos = (
                x,
                y
            )


# =========================================================
# RUDRAA CORE
# =========================================================

class RudraaCore(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.time = 0

        with self.canvas:

            # Outer aura
            Color(
                VIOLET[0],
                VIOLET[1],
                VIOLET[2],
                0.10
            )

            self.aura = Ellipse()

            # Main orbit
            Color(
                CYAN[0],
                CYAN[1],
                CYAN[2],
                0.42
            )

            self.ring1 = Line(
                ellipse=(
                    0,
                    0,
                    dp(125),
                    dp(125)
                ),
                width=1.3
            )

            # Second orbit
            Color(
                ROSE[0],
                ROSE[1],
                ROSE[2],
                0.32
            )

            self.ring2 = Line(
                ellipse=(
                    0,
                    0,
                    dp(88),
                    dp(88)
                ),
                width=1
            )

            # Third-eye inspired center
            Color(
                ROSE[0],
                ROSE[1],
                ROSE[2],
                0.85
            )

            self.eye = Ellipse()

            # Inner energy
            Color(
                CYAN[0],
                CYAN[1],
                CYAN[2],
                0.75
            )

            self.energy = Ellipse()

            # Trishul-inspired geometry
            Color(
                GOLD[0],
                GOLD[1],
                GOLD[2],
                0.55
            )

            self.trishul = Line(
                points=[],
                width=1
            )

        self.bind(
            pos=self.update_core,
            size=self.update_core
        )

        Clock.schedule_interval(
            self.animate,
            1 / 24.0
        )

    def update_core(self, *args):
        pass

    def animate(self, dt):

        self.time += dt

        cx = self.center_x
        cy = self.center_y

        pulse = (
            math.sin(self.time * 2.0) + 1
        ) / 2

        # Outer aura breathing
        aura_size = dp(
            140 + pulse * 24
        )

        self.aura.size = (
            aura_size,
            aura_size
        )

        self.aura.pos = (
            cx - aura_size / 2,
            cy - aura_size / 2
        )

        # Main orbit
        ring_size = dp(112)

        self.ring1.ellipse = (
            cx - ring_size / 2,
            cy - ring_size / 2,
            ring_size,
            ring_size
        )

        # Second orbit
        inner = dp(78)

        self.ring2.ellipse = (
            cx - inner / 2,
            cy - inner / 2,
            inner,
            inner
        )

        # Third eye
        eye_w = dp(
            22 + pulse * 5
        )

        eye_h = dp(
            9 + pulse * 3
        )

        self.eye.size = (
            eye_w,
            eye_h
        )

        self.eye.pos = (
            cx - eye_w / 2,
            cy - eye_h / 2
        )

        # Central energy
        energy_size = dp(
            8 + pulse * 4
        )

        self.energy.size = (
            energy_size,
            energy_size
        )

        self.energy.pos = (
            cx - energy_size / 2,
            cy - energy_size / 2
        )

        # Minimal trishul-inspired form
        top = cy + dp(29)
        bottom = cy - dp(29)

        self.trishul.points = [

            cx,
            bottom,

            cx,
            top,

            cx,
            top,

            cx - dp(8),
            top - dp(9),

            cx,
            top + dp(4),

            cx + dp(8),
            top - dp(9),

            cx,
            top + dp(4)
        ]


# =========================================================
# MESSAGE
# =========================================================

class MessageBubble(BoxLayout):

    def __init__(self, text, user=False, **kwargs):

        super().__init__(
            orientation="vertical",
            size_hint_y=None,
            padding=[
                dp(13),
                dp(9),
                dp(13),
                dp(9)
            ],
            spacing=dp(3),
            **kwargs
        )

        color = (
            USER_PANEL
            if user
            else AI_PANEL
        )

        accent = (
            ROSE
            if user
            else CYAN
        )

        sender = (
            "YOU"
            if user
            else "RUDRAA"
        )

        with self.canvas.before:

            Color(*color)

            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(15)]
            )

            Color(
                accent[0],
                accent[1],
                accent[2],
                0.30
            )

            self.border = Line(
                rounded_rectangle=(
                    self.x,
                    self.y,
                    self.width,
                    self.height,
                    dp(15)
                ),
                width=0.7
            )

        self.sender = Label(
            text=sender,
            font_size=sp(8),
            bold=True,
            color=accent,
            size_hint_y=None,
            height=dp(15),
            halign="left"
        )

        self.body = Label(
            text=text,
            font_size=sp(13.5),
            color=WHITE,
            halign="left",
            valign="top",
            size_hint_y=None
        )

        self.body.bind(
            width=self.set_text_width
        )

        self.body.bind(
            texture_size=self.set_body_height
        )

        self.add_widget(self.sender)
        self.add_widget(self.body)

        self.opacity = 0

        self.bind(
            pos=self.update_graphics,
            size=self.update_graphics
        )

        Clock.schedule_once(
            self.show_message,
            0.03
        )

    def set_text_width(self, instance, width):

        instance.text_size = (
            width,
            None
        )

    def set_body_height(self, instance, value):

        self.body.height = value[1]

        self.height = (
            value[1]
            + dp(27)
        )

    def update_graphics(self, *args):

        self.rect.pos = self.pos
        self.rect.size = self.size

        self.border.rounded_rectangle = (
            self.x,
            self.y,
            self.width,
            self.height,
            dp(15)
        )

    def show_message(self, *args):

        Animation(
            opacity=1,
            duration=0.22,
            t="out_quad"
        ).start(self)


# =========================================================
# MAIN APP
# =========================================================

class RudraaApp(App):

    def build(self):

        self.title = "Rudraa"

        self.client = None
        self.history = []

        root = AnimatedBackground()

        main = BoxLayout(
            orientation="vertical",
            padding=[
                dp(14),
                dp(10),
                dp(14),
                dp(9)
            ],
            spacing=dp(7)
        )

        # =================================================
        # TOP BRAND
        # =================================================

        header = BoxLayout(
            size_hint_y=None,
            height=dp(63)
        )

        left = BoxLayout(
            orientation="vertical",
            size_hint_x=0.68
        )

        title = Label(
            text="R U D R A A",
            font_size=sp(23),
            bold=True,
            color=WHITE,
            halign="left",
            valign="middle"
        )

        subtitle = Label(
            text="EMOTION  -  CONTEXT  -  UNDERSTANDING",
            font_size=sp(7.5),
            color=MUTED,
            halign="left"
        )

        left.add_widget(title)
        left.add_widget(subtitle)

        right = BoxLayout(
            orientation="vertical",
            size_hint_x=0.32
        )

        developed = Label(
            text="DEVELOPED BY",
            font_size=sp(7),
            bold=True,
            color=CYAN,
            halign="right"
        )

        aman = Label(
            text="A M A N",
            font_size=sp(13),
            bold=True,
            color=WHITE,
            halign="right"
        )

        right.add_widget(developed)
        right.add_widget(aman)

        header.add_widget(left)
        header.add_widget(right)

        main.add_widget(header)

        # =================================================
        # CORE PANEL
        # =================================================

        core_panel = GlassPanel(
            orientation="vertical",
            size_hint_y=None,
            height=dp(142),
            padding=[
                dp(5),
                dp(3)
            ]
        )

        self.core = RudraaCore(
            size_hint_y=None,
            height=dp(105)
        )

        core_panel.add_widget(
            self.core
        )

        philosophy = Label(
            text="UNDERSTAND FIRST. RESPOND SECOND.",
            font_size=sp(8),
            bold=True,
            color=MUTED,
            size_hint_y=None,
            height=dp(20)
        )

        core_panel.add_widget(
            philosophy
        )

        main.add_widget(
            core_panel
        )

        # =================================================
        # EMOTION CHIPS
        # =================================================

        chips = BoxLayout(
            size_hint_y=None,
            height=dp(30),
            spacing=dp(6)
        )

        for text in [
            "CALM",
            "OPEN",
            "HEARD",
            "REFLECT"
        ]:

            chip = Button(
                text=text,
                font_size=sp(8),
                bold=True,
                color=WHITE,
                background_normal="",
                background_color=(
                    0.10,
                    0.045,
                    0.17,
                    1
                )
            )

            chips.add_widget(chip)

        main.add_widget(chips)

        # =================================================
        # CHAT TITLE
        # =================================================

        chat_header = BoxLayout(
            size_hint_y=None,
            height=dp(23)
        )

        space = Label(
            text="YOUR SPACE",
            font_size=sp(9),
            bold=True,
            color=WHITE,
            halign="left"
        )

        listening = Label(
            text="RUDRAA IS LISTENING",
            font_size=sp(7),
            color=CYAN,
            halign="right"
        )

        chat_header.add_widget(space)
        chat_header.add_widget(listening)

        main.add_widget(chat_header)

        # =================================================
        # CHAT
        # =================================================

        self.scroll = ScrollView(
            do_scroll_x=False,
            bar_width=dp(3)
        )

        self.chat = GridLayout(
            cols=1,
            spacing=dp(8),
            padding=[
                dp(2),
                dp(3),
                dp(2),
                dp(7)
            ],
            size_hint_y=None
        )

        self.chat.bind(
            minimum_height=self.chat.setter(
                "height"
            )
        )

        self.scroll.add_widget(
            self.chat
        )

        main.add_widget(
            self.scroll
        )

        # =================================================
        # INPUT
        # =================================================

        input_panel = GlassPanel(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(55),
            padding=dp(6),
            spacing=dp(6),
            bg=(
                0.065,
                0.035,
                0.12,
                0.98
            )
        )

        self.input = TextInput(
            hint_text="Tell Rudraa what's going on...",
            multiline=False,
            font_size=sp(13),
            foreground_color=WHITE,
            hint_text_color=MUTED,
            cursor_color=CYAN,
            background_normal="",
            background_active="",
            background_color=(
                0.025,
                0.018,
                0.055,
                1
            ),
            padding=[
                dp(10),
                dp(8)
            ],
            size_hint_x=0.78
        )

        self.input.bind(
            on_text_validate=self.send_message
        )

        send = Button(
            text="SEND",
            font_size=sp(9),
            bold=True,
            color=WHITE,
            background_normal="",
            background_color=VIOLET,
            size_hint_x=0.22
        )

        send.bind(
            on_release=self.send_message
        )

        input_panel.add_widget(
            self.input
        )

        input_panel.add_widget(
            send
        )

        main.add_widget(
            input_panel
        )

        root.add_widget(
            main
        )

        # =================================================
        # FIRST MESSAGE
        # =================================================

        Clock.schedule_once(
            lambda dt: self.add_message(
                "I am Rudraa. You don't have to explain everything perfectly. Start wherever it feels easiest.",
                False
            ),
            0.5
        )

        Clock.schedule_once(
            lambda dt: self.show_api_popup(),
            1.0
        )

        return root

    # =====================================================
    # API POPUP
    # =====================================================

    def show_api_popup(self):

        box = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        info = Label(
            text=(
                "Connect Rudraa with your OpenAI API key.\n"
                "Keep your key private."
            ),
            color=WHITE,
            font_size=sp(11),
            halign="left",
            size_hint_y=None,
            height=dp(50)
        )

        key_input = TextInput(
            hint_text="Enter API key",
            password=True,
            multiline=False,
            font_size=sp(12),
            foreground_color=WHITE,
            hint_text_color=MUTED,
            background_normal="",
            background_color=(
                0.025,
                0.018,
                0.055,
                1
            ),
            padding=[
                dp(10),
                dp(9)
            ]
        )

        connect = Button(
            text="CONNECT RUDRAA",
            font_size=sp(10),
            bold=True,
            color=WHITE,
            background_normal="",
            background_color=VIOLET,
            size_hint_y=None,
            height=dp(44)
        )

        box.add_widget(info)
        box.add_widget(key_input)
        box.add_widget(connect)

        popup = Popup(
            title="RUDRAA CONNECTION",
            content=box,
            size_hint=(0.90, None),
            height=dp(245),
            auto_dismiss=False
        )

        def connect_now(*args):

            key = key_input.text.strip()

            if not key:

                info.text = (
                    "Please enter your API key."
                )

                return

            connect.disabled = True
            connect.text = "CONNECTING..."

            try:

                self.client = OpenAI(
                    api_key=key
                )

                popup.dismiss()

                self.add_message(
                    "Rudraa is connected. I'm listening.",
                    False
                )

            except Exception:

                connect.disabled = False
                connect.text = "TRY AGAIN"

                info.text = (
                    "Connection failed. Check the key."
                )

        connect.bind(
            on_release=connect_now
        )

        popup.open()

    # =====================================================
    # MESSAGE
    # =====================================================

    def add_message(self, text, user=False):

        bubble = MessageBubble(
            text=text,
            user=user
        )

        self.chat.add_widget(
            bubble
        )

        Clock.schedule_once(
            lambda dt: self.scroll_bottom(),
            0.15
        )

    def scroll_bottom(self):

        try:
            self.scroll.scroll_y = 0
        except Exception:
            pass

    # =====================================================
    # SEND
    # =====================================================

    def send_message(self, *args):

        text = self.input.text.strip()

        if not text:
            return

        self.input.text = ""

        self.add_message(
            text,
            True
        )

        self.history.append({
            "role": "user",
            "content": text
        })

        if not self.client:

            self.add_message(
                "Rudraa is not connected yet.",
                False
            )

            return

        self.input.disabled = True

        threading.Thread(
            target=self.ask_ai,
            daemon=True
        ).start()

    # =====================================================
    # RUDRAA AI
    # =====================================================

    def ask_ai(self):

        try:

            instructions = """
You are Rudraa, a highly emotionally intelligent conversational AI.

CORE PRINCIPLE:
UNDERSTAND FIRST. RESPOND SECOND.

Rudraa should understand people beyond literal words.

Internally consider:
- what they literally said
- what they may be feeling
- possible hidden emotions
- trigger
- context
- mixed emotions
- uncertainty
- possible underlying need
- what they may be unable to say directly

Never reveal hidden chain-of-thought.

Behavior:

1. Never claim certainty about someone's feelings.
2. Separate facts from interpretation.
3. Notice indirect communication.
4. Understand Hinglish naturally.
5. Match the user's language and tone.
6. Sound warm, natural and perceptive.
7. Do not sound robotic.
8. Do not immediately give advice when the person mainly needs understanding.
9. Ask a question only when useful.
10. Never diagnose mental illness.
11. Keep normal replies concise but meaningful.
12. Recognize mixed emotions.
13. Do not simply repeat the user's message.
14. Don't use fixed repetitive templates.
15. Make the user feel understood rather than analyzed.

If the user is unclear, explore gently instead of assuming.
"""

            response = self.client.responses.create(
                model="gpt-5.6-luna",
                instructions=instructions,
                input=self.history
            )

            answer = response.output_text.strip()

            if not answer:
                answer = "I'm listening. Tell me a little more."

            self.history.append({
                "role": "assistant",
                "content": answer
            })

            Clock.schedule_once(
                lambda dt, a=answer:
                self.ai_done(a),
                0
            )

        except Exception as e:

            print("RUDRAA ERROR:", e)

            Clock.schedule_once(
                lambda dt: self.ai_error(),
                0
            )

    # =====================================================
    # RESPONSE
    # =====================================================

    def ai_done(self, answer):

        self.input.disabled = False

        self.add_message(
            answer,
            False
        )

    def ai_error(self):

        self.input.disabled = False

        self.add_message(
            "I couldn't connect right now. Please check your internet connection or API key.",
            False
        )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    RudraaApp().run()