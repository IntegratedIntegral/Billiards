from settings import *

class UI:
    def __init__(self):
        self.font = pg.font.SysFont("arial", 22)
        self.hits = 0
        
        self.end_reached = False
    
    @property
    def hits(self):
        return self._hits

    @hits.setter
    def hits(self, val):
        self._hits = val
        self.hits_text = self.font.render("hits: " + str(self._hits), False, (0, 0, 0))
    
    @property
    def end_reached(self):
        return self._end_reached

    @end_reached.setter
    def end_reached(self, val):
        self._end_reached = val
        if val:
            self.set_end_text()

    def set_end_text(self):
        self.end_text = self.font.render(f"Congratulations, you won in {self._hits} hits", False, (0, 0, 0))
    
    def update(self, window):
        window.blit(self.hits_text, (90, 5))
        if self._end_reached:
            window.blit(self.end_text, ((WINDOW_WIDTH - self.end_text.size[0]) // 2, (WINDOW_HEIGHT - self.end_text.size[1]) // 2))