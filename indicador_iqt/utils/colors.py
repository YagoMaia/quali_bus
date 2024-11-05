class Colors:
    RED = '#d62728'
    BLUE = '#1f77b4'
    ORANGE = '#ff7f0e'
    GREEN = '#2ca02c'
    PURPLE = '#9467bd'
    BROWN = '#8c564b'
    PINK = '#e377c2'
    GREY = '#7f7f7f'
    YELLOW = '#bcbd22'
    CYAN = '#17becf'
    
def color_iqt(iqt):
    if iqt >= 3.0:
        return Colors.GREEN
    elif 2 <= iqt < 3.0:
        return Colors.BLUE
    elif 1.0 <= iqt < 2:
        return Colors.RED
    else:
        return Colors.PINK