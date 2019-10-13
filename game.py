#!/usr/bin/env python3
# -*- coding utf-8 -*-

from tkinter impor *
from tkinter import scrolledtext

class five(object):
    
    def __init__(self, game_manager, player1, player2):
        
        self.game = game_manager
        self.players = [None, player1, player2]
        self.height = self.game.dimension
        self.wifth = self.game.dimension
