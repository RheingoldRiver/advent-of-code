for i, row in enumerate(self.cleaned_data):
    for j, char in enumerate(row):
        left = 0
        right = 0
        above = 0
        below = 0
        # don't look at pipe in the actual real pipe
        if char != '.':
            continue
        for k in range(i):
            cell = self.cleaned_data[k][j]
            if cell != '.' and cell != '|':
                above += 1
        for k in range(i, len(self.cleaned_data)):
            cell = self.cleaned_data[k][j]
            if cell != '.' and cell != '|':
                below += 1
        for k in range(j):
            cell = self.cleaned_data[i][k]
            if cell != '.' and cell != '_':
                left += 1
        for k in range(j, len(self.cleaned_data[0])):
            cell = self.cleaned_data[i][k]
            if cell != '.' and cell != '_':
                right += 1
        if above % 2 == 1 and left % 2 == 1 and right % 2 == 1 and below % 2 == 1:
            print(f'found success: row {i} col {j}')
            self.data[i][j] = 'X'
            count += 1