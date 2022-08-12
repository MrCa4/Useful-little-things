
"""
Convenient to use for various queries and connections
"""


def MrCa4Repeater(repeat_count=10, exit_=False):
    def decorator_maker(func):
        def wrapper(*args, **kwargs):
            for i in range(repeat_count):
                try:
                    result = func(*args, **kwargs)
                    break
                except:
                    continue
            else:
                print("All attempts have been exhausted")
                if exit_:
                    exit(1)
                return Exception
            return result

        return wrapper

    return decorator_maker
