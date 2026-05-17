import functions

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.animation import Animation
from kivy.uix.widget import Widget


# ---------------- THEME COLORS (DARK MODE) ----------------
BG_COLOR = (0.08, 0.08, 0.08, 1)
CARD_COLOR = (0.15, 0.15, 0.15, 1)
TEXT_COLOR = (1, 1, 1, 1)


class TaskCard(BoxLayout):

    def __init__(self, text, completed=False, select_callback=None, delete_callback=None, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=60, padding=10, spacing=10, **kwargs)

        self.text = text
        self.select_callback = select_callback
        self.delete_callback = delete_callback

        # Checkbox (completed task)
        self.checkbox = CheckBox(active=completed)
        self.checkbox.bind(active=self.toggle_done)

        # Task label
        self.label = Button(
            text=text,
            background_color=CARD_COLOR,
            color=TEXT_COLOR
        )
        self.label.bind(on_press=self.select_task)

        # Delete button (acts like swipe delete alternative)
        self.delete_btn = Button(text="🗑", size_hint_x=0.2)
        self.delete_btn.bind(on_press=self.delete_task)

        self.add_widget(self.checkbox)
        self.add_widget(self.label)
        self.add_widget(self.delete_btn)

        self.animate_in()

    # -------- Animation (Add effect) --------
    def animate_in(self):
        self.opacity = 0
        anim = Animation(opacity=1, duration=0.3)
        anim.start(self)

    # -------- Select task --------
    def select_task(self, instance):
        if self.select_callback:
            self.select_callback(self.text)

    # -------- Delete task --------
    def delete_task(self, instance):
        if self.delete_callback:
            self.delete_callback(self.text)

    # -------- Completed toggle --------
    def toggle_done(self, checkbox, value):
        if value:
            self.label.color = (0.5, 1, 0.5, 1)
        else:
            self.label.color = TEXT_COLOR


class TaskUI(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)

        self.selected_task = None

        # Title
        self.title = Label(
            text="Task Manager",
            font_size=22,
            color=TEXT_COLOR,
            size_hint=(1, 0.1)
        )

        # Input
        self.input_box = TextInput(
            hint_text="Enter task...",
            size_hint=(1, 0.1),
            multiline=False
        )

        # Buttons
        self.add_btn = Button(text="Add", background_color=(0, 0.6, 0.3, 1))
        self.edit_btn = Button(text="Edit", background_color=(0.2, 0.4, 0.8, 1))

        self.add_btn.bind(on_press=self.add_task)
        self.edit_btn.bind(on_press=self.edit_task)

        btn_box = BoxLayout(size_hint=(1, 0.1), spacing=10)
        btn_box.add_widget(self.add_btn)
        btn_box.add_widget(self.edit_btn)

        # Task list
        self.task_list = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))

        self.scroll = ScrollView()
        self.scroll.add_widget(self.task_list)

        # Add UI
        self.add_widget(self.title)
        self.add_widget(self.input_box)
        self.add_widget(btn_box)
        self.add_widget(self.scroll)

        self.load_tasks()

    # -------- Load tasks --------
    def load_tasks(self):
        self.task_list.clear_widgets()
        tasks = functions.get_task()

        for t in tasks:
            text = t.strip()
            if text:
                card = TaskCard(
                    text=text,
                    select_callback=self.select_task,
                    delete_callback=self.delete_task
                )
                self.task_list.add_widget(card)

    # -------- Select --------
    def select_task(self, text):
        self.selected_task = text
        self.input_box.text = text

    # -------- Add task animation --------
    def add_task(self, instance):
        text = self.input_box.text.strip()
        if not text:
            return

        tasks = functions.get_task()
        tasks.append(text + "\n")
        functions.write_tasks(tasks)

        self.input_box.text = ""

        self.flash_button(self.add_btn)
        self.load_tasks()

    # -------- Edit task animation --------
    def edit_task(self, instance):
        if not self.selected_task:
            return

        tasks = functions.get_task()

        index = tasks.index(self.selected_task + "\n")
        tasks[index] = self.input_box.text + "\n"

        functions.write_tasks(tasks)

        self.input_box.text = ""
        self.selected_task = None

        self.flash_button(self.edit_btn)
        self.load_tasks()

    # -------- Delete task (swipe alternative) --------
    def delete_task(self, text):
        tasks = functions.get_task()
        try:
            tasks.remove(text + "\n")
        except:
            pass

        functions.write_tasks(tasks)
        self.load_tasks()

    # -------- Button animation --------
    def flash_button(self, button):
        anim = Animation(opacity=0.5, duration=0.1) + Animation(opacity=1, duration=0.1)
        anim.start(button)


class TaskApp(App):
    def build(self):
        return TaskUI()


TaskApp().run()