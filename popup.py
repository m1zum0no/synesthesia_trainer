from tkinter import Toplevel, Scrollbar, font
from tkinter.constants import BROWSE, END
from tkinter.ttk import Treeview, Style
from typing import Callable, Iterable


class Popup(Toplevel):
    _item_selected_callback: Callable[[str], None]
    _item_inserted_callback: Callable[[Treeview, str, str], None]

    def _item_selected(self, event):
        items_treeview = event.widget
        selected_item = items_treeview.item(items_treeview.selection()).get('text')

        if self._item_selected_callback:
            self._item_selected_callback(selected_item)

        self.withdraw()

    def _initialize_content(self):
        style = Style()

        default_font = font.nametofont('TkDefaultFont')

        tw = Treeview(self, show='tree', selectmode=BROWSE, style='popup.Treeview')
        tw.grid(row=1, column=0)

        max_font_width = default_font.measure(self.title()) + 40
        for item in self._items:
            item_tag = item.replace(' ', '_')
            item_id = tw.insert('', END, text=item, tags=(item_tag,))
            if self._item_inserted_callback:
                self._item_inserted_callback(tw, item_id, item_tag)

            font_family = font.nametofont('TkDefaultFont').actual()['family']
            font_size = font.nametofont('TkDefaultFont').actual()['size']

            font_str = tw.tag_configure(item_tag)['font']
            if font_str != '':
                font_family, font_size = font_str.split('}') if '{' in font_str else font_str.split(' ')
                font_family = font_family.strip('{} ')
                font_size = int(font_size)

            # adjusting dimensions of the cells to fit various fonts
            font_to_measure = font.Font(family=font_family, size=font_size) if font_str else default_font
            font_height = font_to_measure.metrics("linespace")

            style.configure('popup.Treeview', rowheight=font_height + 10)
            font_width = font_to_measure.measure(item)
            # basing the window width on the parameters of the widest font
            max_font_width = max(max_font_width, font_width)
        tw.column('#0', width=max_font_width + 40)
        # freeze window size configuration

        fonts_scrollbar = Scrollbar(self, orient='vertical', command=tw.yview)
        fonts_scrollbar.grid(row=1, column=0, sticky='nse')
        tw.configure(yscroll=fonts_scrollbar.set)

        # save changes and close the popup window
        tw.bind('<Double-Button-1>', self._item_selected)
        tw.bind('<Return>', self._item_selected)

    def _on_exit(self, *args, **kwargs):
        self.withdraw()

    def __init__(self, *args,
                 title: str, resizable_x=False, resizable_y=False,
                 item_selected_callback: Callable[[str], None] = None,
                 item_inserted_callback: Callable[[Treeview, str, str], None] = None,
                 items: Iterable[str] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.withdraw()
        self.title(title)
        self.resizable(resizable_x, resizable_y)
        self.protocol('WM_DELETE_WINDOW', self._on_exit)
        self.bind('<Escape>', self._on_exit)

        self._item_selected_callback = item_selected_callback
        self._item_inserted_callback = item_inserted_callback
       
        if items is None:
            items = []
        self._items = items

        self._initialize_content()
