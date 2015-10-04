

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ListProperty, \
    BooleanProperty, StringProperty
from kivy.utils import get_color_from_hex, boundary
import random
from kivy.animation import Animation

# google material colors
RED = '#F44336'
PINK = '#E91E63'
PURPLE = '#9C27B0'
DEEP_PURPLE = '#673AB7'
INDIGO = '#3F51B5'
BLUE = '#2196F3'
LIGHT_BLUE = '#03A9F4'
CYAN = '#00BCD4'
TEAL = '#009688'
GREEN = '#4CAF50'
LIGHT_GREEN = '#8BC34A'
LIME = '#CDDC39'
YELLOW = '#FFEB3B'
AMBER = '#FFC107'
ORANGE = '#FF9800'
DEEP_ORANGE = '#FF5722'
BROWN = '#795548'
GREY = '#9E9E9E'
DEEP_GREY = '#607D8B'
WHITE = '#FFFFFF'
BLACK = '#000000'
ALPHA = '#00000000'

SIZE = 8
COLORS = [
    RED,
    PINK,
    PURPLE,
    DEEP_PURPLE,
    INDIGO,
    BLUE,
    LIGHT_BLUE,
    CYAN,
    TEAL,
    GREEN,
    LIGHT_GREEN,
    LIME,
    YELLOW,
    AMBER,
    ORANGE,
    DEEP_ORANGE,
    BROWN,
    GREY,
    DEEP_GREY,
]


Builder.load_string("""
<Atom>:
    spacing: 10
    canvas.before:
        Color:
            rgba: self.bg_color
        Ellipse:
            #pos: self.pos
            #size: self.size
            pos: self.x - self.spacing, self.y - self.spacing
            size: self.width + 2 * self.spacing, self.height + 2 * self.spacing
    canvas:
        Color:
            rgba: self.bg_color
        Ellipse:
            pos: self.x + self.spacing, self.y + self.spacing
            size: self.width - 2 * self.spacing, self.height - 2 * self.spacing
        Color:
            rgb: self.color
        Ellipse:
            pos: self.x + 1.5 * self.spacing, self.y + 1.5 * self.spacing
            size: self.width - 3 * self.spacing, self.height - 3 * self.spacing
    Label:
        color: self.color
        pos: root.x + root.spacing, root.y + root.spacing
        size: root.width - 2 * root.spacing, root.height - 2 * root.spacing
        text: "{}".format(root.atom)

<GameLayout>:
    BoardLayout:
        # size: 100, 100
        canvas:
            Color:
                rgba: self.bg_color
            Rectangle:
                pos: self.pos
                size: self.size

        GameBoard:
            id: board
""")


class Atom(Widget):
    bg_color = ListProperty(get_color_from_hex(ALPHA))
    color = ListProperty(get_color_from_hex(BLACK))
    atom = StringProperty("")
    selected = BooleanProperty(False)
    spacing = NumericProperty(0)

    def select(self):
        if not self.selected:
            Animation(bg_color=self.color, d=0.2).start(self)
            self.selected = True

    def unselect(self):
        if self.selected:
            Animation(bg_color=get_color_from_hex(ALPHA), d=0.2).start(self)
            self.selected = False


class GameLayout(RelativeLayout):
    pass


class GameBoard(Widget):
    selection = ListProperty([])

    def __init__(self, **kwargs):
        super(GameBoard, self).__init__(**kwargs)
        self.items = []
        self.generate()
        self.bind(pos=self.on_pos_size, size=self.on_pos_size)

    def generate(self):
        for ix in range(SIZE):
            for iy in range(SIZE):
                atom = Atom(pos=self.index_to_pos(ix, iy),
                            size=(self.item_size, self.item_size),
                            color=get_color_from_hex(random.choice(COLORS)),
                            atom=random.choice(["Na", "Cl", "O", "H"]))
                self.items.append(atom)
                self.add_widget(atom)

    def on_pos_size(self, *args):
        for ix in range(SIZE):
            for iy in range(SIZE):
                item = self.items[self.item_index(ix, iy)]
                item.pos = self.index_to_pos(ix, iy)
                item.size = (self.item_size, self.item_size)

    def item_index(self, ix, iy):
        return ix * SIZE + iy

    @property
    def item_size(self):
        return int(self.width / SIZE)

    def index_to_pos(self, ix, iy):
        return self.x + ix * self.item_size, self.y + iy * self.item_size

    def find_indeces(self, x, y):
        # relative to widget
        x -= self.x
        y -= self.y
        size = self.item_size

        return (boundary(0, SIZE, int(x / size)),
                boundary(0, SIZE, int(y / size)))

    def select_item(self, touch):
        ix, iy = self.find_indeces(*touch.pos)
        item_index = self.item_index(ix, iy)
        item = self.items[item_index]

        if touch.ud.get('item_index', None) == item_index:
            return

        if self.selection and self.selection[-1] == item_index:
            item.unselect()
            self.selection = self.selection[:-1]
        elif item_index not in self.selection:
            item.select()
            self.selection.append(item_index)
        touch.ud['item_index'] = item_index

    def unselect_all(self):
        for item_index in self.selection:
            self.items[item_index].unselect()
        self.selection = []

    def check(self):
        return False

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        touch.grab(self)
        self.select_item(touch)

        return True

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return
        if not self.collide_point(*touch.pos):
            return
        self.select_item(touch)

    def on_touch_up(self, touch):
        if self.selection:
            if not self.check():
                self.parent.error_animation()
        self.unselect_all()
        touch.ungrab(self)


class BoardLayout(FloatLayout):
    bg_color = ListProperty(get_color_from_hex(WHITE))

    def do_layout(self, *args):
        size = self.width if self.width < self.height else self.height
        for child in self.children:
            child.size = size, size
            child.center = self.center

    def error_animation(self):
        anim = Animation(bg_color=get_color_from_hex(RED),
                         transition="in_bounce", d=0.5) + \
            Animation(bg_color=get_color_from_hex(WHITE),
                      transition="out_sine", d=0.5)
        anim.start(self)


class GameApp(App):
    def build(self):
        return GameLayout()


if __name__ == "__main__":
    GameApp().run()
