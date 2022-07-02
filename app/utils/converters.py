def int_to_color(count: int):
    match count:
        case c if c in range(3):
            return "#d5d8f2"
        case c if c in range(6):
            return "#959bd0"
        case c if c in range(11):
            return "#aaaed3"
        case c if c in range(20):
            return "#979ac6"
        case c if c in range(30):
            return "#6f739a"
        case c if c in range(50):
            return "#4c5285"
        case c if c in range(75):
            return "#393f7a"
        case _:
            return "#2c326a"
