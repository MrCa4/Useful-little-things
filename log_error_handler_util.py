import logging
import sys


# You should only put decorator
# @class_decorator_method()
# on class

def log_and_error_handler_decorator_maker(func) -> dict:
    def wrapper(self, *args, **kwargs) -> object:
        try:
            function_name = func.__name__
            result = func(self, *args, **kwargs)
        except self.error_object as err:
            error_msg = {'result': False, 'action_type': function_name, 'error': str(err)}
            logging.error(error_msg)
            return error_msg
        except self.warning_object as warning:
            warning_msg = {'result': False, 'action_type': function_name, 'error': str(warning)}
            logging.warning(warning_msg)
            return warning_msg
        except Exception as unhandled_exception:
            critical_msg = {'result': False, 'action_type': function_name, 'error': str(unhandled_exception)}
            logging.error(critical_msg)
            return critical_msg
        else:
            try:
                logging.info(str(result)[:1000] + "...")
            except Exception as exp:
                logging.info(str(result.get('result') + result.get('action_type')) + "...")
            return result

    return wrapper


def class_decorator_method(decorator=log_and_error_handler_decorator_maker,
                           error_object=Exception,
                           warning_object=Exception):
    def decorate(cls):
        init = getattr(cls, '__init__')
        print(init)
        init_code = init.__code__
        original_locals_count = init_code.co_nlocals
        original_co_names = init_code.co_names
        original_code = init_code.co_code
        #init_code = init_code.replace(co_consts=(None, 1,))
        init_code = init_code.replace(co_nlocals=original_locals_count + 2)
        print(init_code.co_names)
        print(Exception.__name__)
        init_code = init_code.replace(
            co_names=original_co_names.__add__((error_object.__name__, warning_object.__name__, 'error_object', 'warning_object',)))
        print(init_code.co_names)
        # init_code.co_names.find()
        # TODO
        init_code =init_code.replace(co_code=b't\x00|\x00_\x01t\x01|\x00_\x02' + original_code)
        init.__code__ = init_code
        setattr(cls, '__init__', init)

        for attr in cls.__dict__:
            if callable(getattr(cls, attr)) and not attr.startswith('__'):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate
