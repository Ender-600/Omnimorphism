def is_heavy(item, *args, **kwargs):
    if isinstance(item, Box):
        if item.mass > 10:
            return True
        else:
            return False
    raise ValueError("Item is not a Box")