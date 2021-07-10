    #!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2021 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#
#
# Pylide 
#   Python3 implementation of Flide (executable)
#
#   github.com/ferhatgec/pylide
#   github.com/ferhatgec/flide


from enum import IntEnum
from sys import argv
from time import sleep


class FlideTokens(IntEnum):
    Begin = 0
    End = 1

    Label = 2
    Wait = 3

    New = 4
    Undef = 5


class Flide:
    def __init__(self, filename: str):
        self.is_begin = False

        self.is_label = False
        self.is_data = False

        self.is_wait = False

        self.is_left = False
        self.is_center = False
        self.is_right = False
        self.is_centerxy = False

        self.label_data = ''
        self.file_data = ''

        self.tokens = []
        self.h, self.w = self.get_terminal_size()

        with open(filename) as data:
            for line in data:
                self.file_data += f'{line}'

    def tokenize(self):
        self.tokens = self.file_data.split(' ')

    def parse(self):
        for token in self.tokens:
            temp_check = token.strip()

            if self.is_begin:
                if self.is_label or self.is_left or self.is_center or self.is_right or self.is_centerxy:
                    if len(token) <= 1:
                        continue

                    if self.is_data:
                        if token.strip().endswith('"'):
                            self.label_data += token
                            self.label_data = self.label_data.strip()[:-1]

                            if self.is_left:
                                self.left(self.label_data)
                            elif self.is_center:
                                self.center(self.label_data)
                            elif self.is_right:
                                self.right(self.label_data)
                            elif self.is_centerxy:
                                self.centerxy(self.label_data)
                            else:
                                print(self.label_data)
                            
                            self.label_data = ''

                            self.is_label = False
                            self.is_left = False
                            self.is_center = False
                            self.is_right = False
                            self.is_centerxy = False
                            self.is_data = False

                            continue

                    if token.startswith('"'):
                        if token.endswith('"'):
                            token = token[:-1]
                            token = token[1:]

                            if self.is_left:
                                self.left(token)
                            elif self.is_center:
                                self.center(token)
                            elif self.is_right:
                                self.right(token)
                            elif self.is_centerxy:
                                self.centerxy(token)
                            else:
                                print(token)
                            
                            self.is_label = False
                            self.is_left = False
                            self.is_center = False
                            self.is_right = False
                            self.is_centerxy = False

                            continue

                        self.is_data = True

                        self.label_data += f'{token[1:]} '
                        continue

                    self.label_data += f'{token} '
                    continue

                if self.is_wait:
                    if token.isnumeric():
                        sleep(float(token))

                    self.is_wait = False
                    continue

                if temp_check == 'End':
                    exit(0)
                elif temp_check == 'Label':
                    self.is_label = True
                elif temp_check == 'Left':
                    self.is_left = True
                elif temp_check == 'Center':
                    self.is_center = True
                elif temp_check == 'Right':
                    self.is_right = True
                elif temp_check == 'CenterXY':
                    self.is_centerxy = True
                elif temp_check == 'Wait':
                    self.is_wait = True
                elif temp_check == 'New':
                    self.clear()
                    self.refresh()

                continue

            if temp_check == 'Begin':
                self.is_begin = True
                self.clear()
                self.refresh()
                self.to_up()
                continue


    def left(self, data: str):
        print(data)
    
    def center(self, data: str):
        for _ in range(0, int(self.w / 3) - 1):
            print(end=' ')

        print(end=f'{data}')

        for _ in range(0, int(self.w / 3)):
            print(end=' ')

    def right(self, data: str):
        for _ in range(0, int(self.w / 1.6)):
            print(end=' ')

        print(data)

    def centerxy(self, data: str):
        for _ in range(0, int(self.h / 2)):
            print(end='\n')
        
        self.center(data)
        
    def begin(self):
        self.is_begin = True
        self.clear()
        self.refresh()
        self.to_up()

    @staticmethod
    def end_exit():
        exit(0)

    def label(self):
        self.is_label = True

    def wait(self):
        self.is_wait = True

    def new(self):
        self.clear()
        self.refresh()

    def undef(self):
        pass

    @staticmethod
    def refresh():
        print(end='\x1b[2J')

    def clear(self):
        self.refresh()
        print(end='\x1b[H')

    @staticmethod
    def to_up():
        print(end='\x1b[0A')

    @staticmethod
    def up_to(n: int):
        print(end=f'\x1b[{n}A')

    @staticmethod
    def disable_cursor():
        print(end='\x1b[?25l')

    @staticmethod
    def enable_cursor():
        print(end='\x1b[?25h')

    @staticmethod
    def get_terminal_size() -> (int, int):
        from fcntl import ioctl
        from struct import pack, unpack
        import termios
        import os

        with open(os.ctermid(), 'r') as fd:
            packed = ioctl(fd, termios.TIOCGWINSZ, pack('HHHH', 0, 0, 0, 0))
            rows, cols, h_pixels, v_pixels = unpack('HHHH', packed)

        return rows, cols

if len(argv) < 2:
    exit(0)

init = Flide(argv[1])
init.tokenize()
init.parse()
