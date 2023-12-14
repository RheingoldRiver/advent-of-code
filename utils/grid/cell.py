class Cell:
    def __init__(self, row: int, col: int, data=None):
        self.row = row
        self.col = col
        self.data = data

    def __repr__(self):
        return f"<Point {str(self.data)} at row {self.row} col {self.col}>"

    def __str__(self):
        return str(self.data['value'])

    @property
    def value(self):
        return self.data.get('value')

    def set_value(self, val):
        self.data['value'] = val
