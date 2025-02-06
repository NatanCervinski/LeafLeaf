from kivy.app import App
from kivy.uix.button import Button


class LeafLeafApp(App):
    def build(self):
        return Button(text="Logar com o Google")


LeafLeafApp().run()
