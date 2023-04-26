class Glyph:
  '''Graphic representation of a character, measurements depend on slant/weight/etc attributes, 
  instances of which are grouped into "fonts" for better coordinates substitution of the 
  incorrectly recognized by Tesseract OCR engine char positions'''
  def __init__(self, w, h):
    self.w = w
    self.h = h 


class Font:
  def __init__(self, char=None, glyph: Glyph=None):
    self.glyphs = {} if not glyph else {char: glyph}


class WordBbox:
  '''Contains list of all characters composing word unit and own rightmost coordinates as Tesseract 
  returns correct position on a word-level'''
  #self.overlap_preceeds_incorrect_coords_affected_chars = []
  #self.incorrect_coords_preceed_overlap_affected_chars = []
  bug_order_unknown = None
  maybe_overlap_follows = None
  #self.maybe_new_font = False
  #self.awaits_glyphs_to_fix_bug = False    

  def expand_font(self):
    for char_bbox in self.chars:
      if char_bbox.corrected_coords:
        continue
      self.font.glyphs.setdefault(char_bbox.char, char_bbox.glyph if hasattr(char_bbox, 'glyph') else Glyph(char_bbox.w, char_bbox.h))

  def switch_font(self, font: Font):
    self.font = font
    # glyphs will be appointed to different font during font expansion

  def assigned_font_differs(self, font: Font):
    other_chars_in_diff_font = False
    for char in self.chars:
      if not (hasattr(char, 'w') or hasattr(char, 'glyph')):
        continue 
      glyph = font.glyphs.get(char.char, char.glyph if hasattr(char, 'glyph') else Glyph(char.w, char.h))
      char_w = char.glyph.w if hasattr(char, 'glyph') else char.w
      char_h = char.glyph.h if hasattr(char, 'glyph') else char.h 
      if (char_w, char_h) != (glyph.w, glyph.h): 
        return False
      else:
        other_chars_in_diff_font = True
    return other_chars_in_diff_font
  
  def changed_font_not_bug_sentinel(self, fonts, char_bbox, w, h):
    for font in fonts:
      glyph = font.glyphs.get(char_bbox.char, None)
      if glyph and (glyph.w, glyph.h) == (w, h):
        if self.assigned_font_differs(font):
          self.switch_font(font)
          return True
    return False

  def __init__(self, x0, y0, x1, y1, previous_font: Font):
    self.x0 = x0 
    self.y0 = y0
    self.x1 = x1
    self.y1 = y1
    self.chars = []
    self.previous_char_bbox = x0
    self.font = previous_font


class CharBbox:
  '''Stores bottom left coordinate of own position on the page and reference 
  to character width and height required by djvumake utility in Glyph class'''
  y1 = None
  x1 = None
  w = None
  h = None
  overlap_preceeds = None
  left_coords_from_next_char = None
  corrected_coords = None

  def validate_gauges(self, word_bbox, w, h):
    glyph = word_bbox.font.glyphs.get(self.char, Glyph(w, h))
    return ((-1 <= (glyph.w - w) <= 1) and (-3 <= (glyph.h - h) <= 3))

  def validate_start_position(self, x0, word_bbox: WordBbox):
    return word_bbox.previous_char_bbox < x0 or word_bbox.x0 == x0
  
  def __init__(self, char, word_bbox: WordBbox, fonts, x0=None, y0=None, x1=None, y1=None):
    self.char = char
    # to skip during font expansion
    if self.char in word_bbox.font.glyphs:
      self.w = word_bbox.font.glyphs[self.char].w

    word_bbox.chars.append(self)

    if not any((x0, y0, x1, y1)):
      # == self.left_coords_from_next_char will be set after init
      return
    
    try:
      prev_char = word_bbox.chars[-2]  
    except IndexError: 
      prev_char = None
         
    if self.validate_start_position(x0, word_bbox):
      if word_bbox.maybe_overlap_follows:
        word_bbox.maybe_overlap_follows = False
      self.x0 = x0
      self.y0 = y0
      w = x1 - self.x0
      h = y1 - y0
      word_bbox.previous_char_bbox = x1
      if not self.validate_gauges(word_bbox, w, h):
        if word_bbox.changed_font_not_bug_sentinel(fonts, self, w, h):
          self.glyph = word_bbox.font.glyphs[self.char]
        else:
          self.corrected_coords = True
          if prev_char and prev_char.left_coords_from_next_char:
            self.overlap_preceeds = True
          elif w > word_bbox.font.glyphs[self.char].w:  
            word_bbox.maybe_overlap_follows = True  
          else:
            self.maybe_left_coords_from_next_char = True
          self.x1 = x1
          self.y1 = y1
          self.w = word_bbox.font.glyphs[self.char].w
          self.h = self.y1 - self.y0
      elif not self.char in word_bbox.font.glyphs:
        self.x1 = x1
        self.y1 = y1
        self.w = w
        self.h = h  
      else:
        self.glyph = word_bbox.font.glyphs[self.char]
    else:
      self.corrected_coords = True
      if self.char in word_bbox.font.glyphs:
        self.w = word_bbox.font.glyphs[self.char].w
      if word_bbox.maybe_overlap_follows:
        # guaranteed that hasattr(prev_char, 'glyph')
        if self.w and (prev_char.x1 - prev_char.x0) >= (prev_char.w + self.w):
          self.y0 = prev_char.y0
          self.x1, prev_char.x1 = prev_char.x1, None
          self.y1 = prev_char.y1
          self.h = self.y1 - self.y0  
          self.x0 = self.x1 - self.w
        elif not self.w:
          print('))))00)))00))))0')
        else:
          prev_char.left_coords_from_next_char = True
          self.overlap_preceeds = True
          prev_char.x0 = x0
          prev_char.y0 = y0
          self.x0 = x1 - self.w
          self.y0 = y0
        word_bbox.maybe_overlap_follows = False
      elif hasattr(prev_char, 'glyph') or (prev_char.corrected_coords and prev_char.char in word_bbox.font.glyphs):
        # previous char is reliably recognized correctly hence current's position starts at the next
        # and the next is either (1) contains positions of current and self
        # (2) only current -> next after that is also wrong
        self.left_coords_from_next_char = True 
      else:
        self.left_coords_from_next_char = True
        #word_bbox.bug_order_unknown = True
        # The order can't be determined reliably
