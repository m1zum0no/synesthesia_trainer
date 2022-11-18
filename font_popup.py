from tkinter import BROWSE, END, Scrollbar, Toplevel, font
from tkinter.ttk import Style, Treeview
from typing import Callable


class FontPopup(Toplevel):
    font_changed_callback: Callable[[str], None]

    def font_changed(self, event):
        font_treeview = event.widget
        selected_font_name = font_treeview.item(font_treeview.selection()).get('text')
        self.font_changed_callback(selected_font_name)
        self.withdraw()

    @staticmethod
    def get_fonts():
        # retrieve all system fonts
        fonts = sorted(set(font.families()))
        # remove Noto Color Emoji font, which causes crashes on some systems
        if 'Noto Color Emoji' in fonts:
            fonts.remove('Noto Color Emoji')
        return fonts

    def _initialize_content(self):
        style = Style()
        font_treeview = Treeview(self, show='tree', selectmode=BROWSE)
        font_treeview.grid(row=1, column=0)
        # to configure the optimal width of the treeview for all font names to fit in fully
        max_font_width = 0
        for font_name in self.get_fonts():
            font_tag = font_name.replace(' ', '_')
            font_treeview.insert('', END, text=font_name, tags=(font_tag,))
            font_treeview.tag_configure(font_tag, font=(font_name, 11))
            # adjusting dimensions of the cells to fit various fonts
            font_to_measure = font.Font(family=font_name, size=11)
            font_height = int(font.Font(font=font_tag).metrics('ascent') * 1.3 \
                          + font.Font(font=font_tag).metrics('descent') * 2)
            ''' exception for a particular problematic font on Linux 
            if font_name == 'MathJax_WinIE6':  # esint10 isn't getting displayed
                # ???
            else: '''
            style.configure('Treeview', rowheight=font_height)
            font_width = font_to_measure.measure(font_name)
            # basing the window width on the parameters of the widest font
            max_font_width = max(max_font_width, font_width)
        font_treeview.column('#0', width=max_font_width + 40)
        # freeze window size configuration

        fonts_scrollbar = Scrollbar(self, orient='vertical', command=font_treeview.yview)
        fonts_scrollbar.grid(row=1, column=0, sticky='nse')
        font_treeview.configure(yscroll=fonts_scrollbar.set)

        # save changes and close the popup window
        font_treeview.bind('<Double-Button-1>', self.font_changed)
        font_treeview.bind('<Return>', self.font_changed)

    def _on_exit(self):
        self.withdraw()

    def __init__(self, *args, font_changed_callback: Callable[[str], None], **kwargs,):
        super().__init__(*args, **kwargs)
        self.withdraw()
        self.title('Выбрать шрифт')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self._on_exit)
        self._initialize_content()
        self.font_changed_callback = font_changed_callback
