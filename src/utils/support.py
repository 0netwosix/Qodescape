#!/usr/bin/python3

from termcolor import colored

class Print:
    # Green text
    @staticmethod
    def dbPrint(colored_message, message):
        print("{colored_message} {message}".format(
            colored_message=colored(colored_message, 'green'),
            message=message
        ))

    # Yellow text
    @staticmethod
    def dbErrorPrint(colored_message, message):
        print("{colored_message} {message}".format(
            colored_message=colored(colored_message, 'yellow'),
            message=message
        ))

    # Red text
    @staticmethod
    def errorPrint(colored_message, message=None):
        print("{colored_message} {message}".format(
            colored_message=colored(colored_message, 'red'),
            message=message
        ))