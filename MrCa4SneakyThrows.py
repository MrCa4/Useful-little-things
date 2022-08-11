import logging


"""

You must only put decorator @MrCa4SneakyThrows() on your class
You may overload error and warning obejcts like this:

        from sqlalchemy import create_engine, exc
        
        @MrCa4SneakyThrows(error_object=exc.SQLAlchemyError, warning_object=exc.SAWarning)
        class A:
            
            def a(self):
                pass
                
"""


def log_and_error_method_decorator(func) -> dict:
    def wrapper(self, *args, **kwargs) -> object:
        try:
            function_name = func.__name__
            result = func(self, *args, **kwargs)
        except self.__error_object as err:
            error_msg = {'result': False, 'action_type': function_name, 'error': str(err)}
            logging.error(error_msg)
            return error_msg
        except self.__warning_object as warning:
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
                logging.info(str(result.get('result')+result.get('action_type')) + "...")
             return result
    return wrapper


def MrCa4SneakyThrows(decorator=log_and_error_method_decorator,
                          error_object=Exception,
                          warning_object=Exception) -> object:
    def decorate(cls):
        setattr(cls,'__error_object',error_object)
        setattr(cls,'__warning_object',warning_object)
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)) and not attr.startswith('__'):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate
