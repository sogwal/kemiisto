

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ListProperty, \
    ObjectProperty
from kivy.utils import get_color_from_hex, boundary
import random
from kivy.animation import Animation

from core.board import Board, BoardItemStatus
from core.molecule import Atom

VERY_SLOW = 2.5
SLOW = 1.0
FAST = 0.5
VERY_FAST = 0.2


class ColorsFactory(object):
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

    class Color(str):
        def __call__(self, alpha=1.0):
            return get_color_from_hex("%s%02x" % (self, 255 * alpha))

    def __init__(self):
        self._colors = [getattr(self, color)
                        for color in dir(ColorsFactory)
                        if color.isupper() and
                        color not in ("WHITE", "BLACK")]

    def __getattribute__(self, name):
        attr = super(ColorsFactory, self).__getattribute__(name)
        if name.isupper():
            return ColorsFactory.Color(attr)
        return attr

    @property
    def colors(self):
        return self._colors


Colors = ColorsFactory()

SIZE = 8


Builder.load_string("""
#:import BoardItemStatus core.board.BoardItemStatus
<AtomWidget>:
    id: atom
    spacing: 10
    opacity: 0.25 if BoardItemStatus.CHECKED == self.status else 1.0
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
        markup: True
        color: self.color
        pos: root.x + root.spacing, root.y + root.spacing
        size: root.width - 2 * root.spacing, root.height - 2 * root.spacing
        text: root.to_string()

<GameRelativeLayout>:
    board: board
    BoardFloatLayout:
        board: board
        # size: 100, 100
        canvas:
            Color:
                rgba: self.bg_color
            Rectangle:
                pos: self.pos
                size: self.size

        GameBoardWidget:
            id: board
""")


class AtomWidget(Widget):
    bg_color = ListProperty(Colors.BLACK(0.0))
    color = ListProperty(Colors.BLACK())
    color_alpha = ListProperty(Colors.BLACK(0.33))
    anim = ObjectProperty(None, allownone=True)
    spacing = NumericProperty(0)
    status = NumericProperty(0)
    core_atom = ObjectProperty(None, rebind=True)

    def to_string(self):
        return u"{}[sub]{}[/sub]".format(
            self.core_atom.atom.atom,
            self.core_atom.atom.number
            if self.core_atom.atom.number > 1 else "")

    def select(self):
        if self.core_atom.status == BoardItemStatus.EMPTY:
            if self.anim:
                self.anim.cancel(self)
                self.anim = None
            self.anim = Animation(bg_color=self.color_alpha, d=FAST)
            self.anim.start(self)
            self.core_atom.marked()
            self.status = BoardItemStatus.MARKED

    def unselect(self):
        if self.core_atom.status == BoardItemStatus.MARKED:
            if self.anim:
                self.anim.cancel(self)
                self.anim = None
            self.anim = Animation(bg_color=Colors.BLACK(0.0), d=VERY_FAST)
            self.anim.start(self)
            self.core_atom.empty()
            self.status = BoardItemStatus.EMPTY

    def deactivate(self):
        self.core_atom.checked()
        self.status = BoardItemStatus.CHECKED

    def collide_point(self, x, y):
        return (self.center_x - x) ** 2 + \
               (self.center_y - y) ** 2 <= \
               ((self.width - 3 * self.spacing) / 2) ** 2


class GameRelativeLayout(RelativeLayout):
    board = ObjectProperty(None)

    def init_game(self):
        self.board.generate()


class GameBoardWidget(Widget):
    selection = ListProperty([])

    def __init__(self, **kwargs):
        super(GameBoardWidget, self).__init__(**kwargs)
        self.items = [None] * SIZE ** 2
        self.core_board = [None] * SIZE ** 2
        self.bind(pos=self.on_pos_size, size=self.on_pos_size)

    def generate(self):
        self.core_board = Board.generate(SIZE, [Atom("Na", 1), Atom("Cl", 1),
                                                Atom("O", 1), Atom("H", 1),
                                                Atom("H", 2), Atom("O", 2)],
                                         )
        for ix in range(SIZE):
            for iy in range(SIZE):
                index = self.item_index(ix, iy)
                color = random.choice(Colors.colors)
                atom = AtomWidget(pos=self.index_to_pos(ix, iy),
                                  size=(self.item_size, self.item_size),
                                  color=color(), color_alpha=color(0.33),
                                  status=self.core_board[index].status,
                                  core_atom=self.core_board[index])
                self.items[index] = atom
                self.add_widget(atom)

    def on_pos_size(self, *args):
        for ix in range(SIZE):
            for iy in range(SIZE):
                item = self.items[self.item_index(ix, iy)]
                if item is None:
                    continue
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

        if not item.collide_point(*touch.pos) or \
                item.status == BoardItemStatus.CHECKED:
            touch.ud['item'] = None
            return

        if touch.ud.get('item', None) == item:
            return

        # if self.selection and not self.selection[-1].core_atom.is_path(item):
        #    return

        if self.selection and self.selection[-1] == item:
            item.unselect()
            self.selection = self.selection[:-1]
        elif item not in self.selection:
            item.select()
            self.selection.append(item)
        touch.ud['item'] = item

    def unselect_all(self):
        for item in self.selection:
            item.unselect()
            item.deactivate()
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
        return True

    def on_touch_up(self, touch):
        if self.selection:
            if not self.check():
                self.parent.error_animation()
        self.unselect_all()
        touch.ungrab(self)
        return True


class BoardFloatLayout(FloatLayout):
    bg_color = ListProperty(Colors.WHITE())
    board = ObjectProperty(None)

    def do_layout(self, *args):
        size = self.width if self.width < self.height else self.height
        self.board.size = size, size
        self.board.center = self.center

    def error_animation(self):
        anim = Animation(bg_color=Colors.RED(),
                         transition="in_bounce", d=FAST) + \
            Animation(bg_color=Colors.WHITE(),
                      transition="out_sine", d=VERY_FAST)
        anim.start(self)


class GameApp(App):
    def build(self):
        self.layout = GameRelativeLayout()
        return self.layout

    def on_start(self):
        self.layout.init_game()


if __name__ == "__main__":
    GameApp().run()
