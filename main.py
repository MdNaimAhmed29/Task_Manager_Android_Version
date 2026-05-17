import functions
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class TaskUI(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.label = Label(text="Add Task")

        self.input_box = TextInput(hint_text="Add your task here")

        self.add_button = Button(text="Add")
        self.edit_button = Button(text="Edit")

        self.add_button.bind(on_press=self.add_task)
        self.edit_button.bind(on_press=self.edit_task)

        # list container
        self.task_list = GridLayout(cols=1, size_hint_y=None)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))

        self.scroll = ScrollView()
        self.scroll.add_widget(self.task_list)

        self.add_widget(self.label)
        self.add_widget(self.input_box)
        self.add_widget(self.add_button)
        self.add_widget(self.scroll)
        self.add_widget(self.edit_button)

        self.selected_task = None

        self.load_tasks()

    def load_tasks(self):
        self.task_list.clear_widgets()
        tasks = functions.get_task()

        for t in tasks:
            task_text = t.strip()

            btn = Button(text=task_text, size_hint_y=None, height=40)
            btn.bind(on_press=self.select_task)
            self.task_list.add_widget(btn)

    def select_task(self, instance):
        self.selected_task = instance.text
        self.input_box.text = instance.text

    def add_task(self, instance):
        new_task = self.input_box.text + "\n"
        tasks = functions.get_task()

        tasks.append(new_task)
        functions.write_tasks(tasks)

        self.input_box.text = ""
        self.load_tasks()

    def edit_task(self, instance):
        if not self.selected_task:
            return

        tasks = functions.get_task()

        index = tasks.index(self.selected_task + "\n")
        tasks[index] = self.input_box.text + "\n"

        functions.write_tasks(tasks)

        self.input_box.text = ""
        self.selected_task = None
        self.load_tasks()


class TaskApp(App):
    def build(self):
        return TaskUI()


TaskApp().run()