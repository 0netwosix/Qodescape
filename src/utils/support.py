from termcolor import colored

class Print:
    ''' Sample output,
        DB output:
        [200]   [DB-Node] FOUND: index_exec
        ------------------------------------
        Normal script output:
        [PASS]  ast Directory created: ../test-projects/test-1/ast

        Output keywords:
        [FAIL] [PASS] [WARN] [SKIP] [INFO] [200] [404]
    '''
    # Green text
    @staticmethod
    def success_print(colored_message, message=''):
        print("{colored_message}\t{message}".format(
            colored_message=colored(colored_message, 'green'),
            message=message
        ))

    # Yellow text
    @staticmethod
    def info_print(colored_message, message=''):
        print("{colored_message}\t{message}".format(
            colored_message=colored(colored_message, 'yellow'),
            message=message
        ))

    # Red text
    @staticmethod
    def error_print(colored_message, message=''):
        print("{colored_message}\t{message}".format(
            colored_message=colored(colored_message, 'red'),
            message=message
        ))

    # Bold white text in red background
    @staticmethod
    def time_print(colored_message, message=''):
        print("{colored_message}\t{message}".format(
            colored_message=colored(colored_message, 'white', 'on_red', ['bold']),
            message=message
        ))

    # No customizations
    @staticmethod
    def clear_print(message=''):
        print("{message}".format(
            message=message
        ))