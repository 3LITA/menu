from django.core.validators import URLValidator, ValidationError


def validate(path):
    val = URLValidator()

    try:
        val(path)
    except ValidationError:
        return True
    else:
        return False


def has_parent(item):
    try:
        parent_id = item['parent_id']
    except KeyError:
        return False
    else:
        return parent_id


def find_active(items, current_url):
    active = items[0]  # root

    for item in items:
        item['children'] = list()

    id_map = {item['id']: item for item in items}

    for item in items:
        item['is_named'] = validate(item['content']) if item['content'] else False
        if item['content'] and item['content'] == current_url:
            active = item

        if has_parent(item):
            parent = id_map[item['parent_id']]
            parent['children'].append(item)
            id_map[parent['id']] = parent

    return id_map, active


def create_path(id_map, active_item):
    path = list()
    item = active_item

    path.append(item)
    while has_parent(item):
        item = id_map[item['parent_id']]
        path.append(item)

    path.reverse()
    return path


def create_sequence(path):
    sequence = list()
    went_down = 0
    for i in range(len(path)):
        sequence.append(path[i])
        if i == len(path) - 1:
            sequence.append('close')
            sequence.insert(-2, 'open')
        sequence.append('down')
        went_down += 1
        sequence += [child for child in path[i]['children'] if child not in path]
    sequence += ['up' for _ in range(went_down)]
    return sequence
