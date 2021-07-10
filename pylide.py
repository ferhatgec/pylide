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

        self.label_data = ''
        self.file_data = ''

        self.tokens = []

        with open(filename) as data:
            for line in data:
                self.file_data += f'{line}'

    def tokenize(self):
        self.tokens = self.file_data.split(' ')

    def parse(self):
        for token in self.tokens:
            temp_check = token.strip()

            if self.is_begin:
                if self.is_label:
                    if len(token) <= 1:
                        continue

                    if self.is_data:
                        if token.strip().endswith('"'):
                            self.label_data += token
                            self.label_data = self.label_data.strip()[:-1]

                            print(self.label_data)
                            self.label_data = ''

                            self.is_label = False
                            self.is_data = False
                            continue

                    if token.startswith('"'):
                        if token.endswith('"'):
                            token = token[:-1]
                            token = token[1:]
                            print(token)
                            self.is_label = False
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


if len(argv) < 2:
    exit(0)

init = Flide(argv[1])
init.tokenize()
init.parse()
