
class MrCa4Singleton:
    instance = None

    def __init__(self, cls):
        self.cls = cls

    def __call__(self, *args, **kwargs):
        if MrCa4Singleton.instance is None:
            MrCa4Singleton.instance = self.cls(*args, **kwargs)
        return MrCa4Singleton.instance
