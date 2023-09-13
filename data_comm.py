class data_reader:

    separator = ','
    separator_equivalent = '[%comma%]'
    headers, columns = [], []
    isComment = False
    comment = ''
    comment_finisher = 'END'

    def scan(self, path):
        with open(path) as file:
            lines = file.readlines()

            starter = 0

            if self.isComment:
                for i in range(len(lines)):
                    if lines[i].replace('\n', '') != self.comment_finisher:
                        self.comment += lines[i]
                    else:
                        starter = i + 1
                        break

            for i in range(starter, len(lines)):
                if lines[i] != '' and lines[i] is not None and lines[i] != '\n':
                    starter = i
                    break

            temp_headers = lines[starter].split(self.separator)
            for h in temp_headers:
                self.headers.append(h.replace('\n', ''))

            for i in range(len(self.headers)):
                self.columns.append([])

            for i in range(starter + 1, len(lines)):
                if lines[i] != '' and lines[i] is not None and lines[i] != '\n':
                    cells = lines[i].split(self.separator)

                    for j in range(len(cells)):
                        self.columns[j].append(cells[j].replace('\n', '').replace(self.separator_equivalent, self.separator))


    def get_md_table(self):
        table = ''

        for i in range(len(self.headers)):
            if table == '':
                table = '| ' + self.headers[i] + ' |'
            else:
                table += ' ' + self.headers[i] + ' |'

        for i in range(len(self.headers)):
            if i == 0:
                table += '\n| --- |'
            else:
                table += ' --- |'

        for i in range(len(self.columns[0])):
            line = ''

            for j in range(len(self.headers)):
                if line == '':
                    line = '| ' + self.columns[j][i] + ' |'
                else:
                    line += ' ' + self.columns[j][i] + ' |'

            table += '\n' + line

        return table

    def get_column(self, header):
        column = []

        if header in self.headers:
            index = self.headers.index(header)
            column = self.columns[index]

        return column

class data_writer:
    separator = ','
    separator_equivalent = '[%comma%]'
    headers, columns = [], []
    _isComment = False
    comment = ''
    comment_finisher = 'END'
    null_text = 'NULL'
    path = ''

    def upload(self, path, isComment):
        file = data_reader()

        file.isComment = isComment
        self._isComment = isComment
        self.path = path
        file.separator = self.separator
        file.separator_equivalent = self.separator_equivalent
        file.comment_finisher = self.comment_finisher

        file.scan(path)

        self.headers = file.headers
        self.columns = file.columns

        if isComment:
            self.comment = file.comment

    def add_column(self, header, column_cells):
        self.headers.append(header)

        if column_cells is not None:
            remains = len(self.columns[0]) - len(column_cells)
            for i in range(remains):
                self.columns[len(self.headers) - 1].append(self.null_text)
        else:
            for i in range(len(self.columns[0])):
                self.columns[len(self.headers) - 1].append(self.null_text)

    def add_row(self, cells):
        for i in range(len(self.headers)):
            if i < len(cells):
                self.columns[i].append(cells[i])
            else:
                self.columns[i].append(self.null_text)

    def add_comment(self, comment):
        self.comment = comment
        self._isComment = True

    def delete_column(self, header):
        if header in self.headers:
            index = self.headers.index(header)

            del self.headers[index]
            del self.columns[index]

    def delete_row(self, index):
        if index < len(self.columns[0]):
           for i in range(len(self.headers)):
               del self.columns[i][index]

    def delete_item(self, x_index, y_index):
        self.columns[x_index][y_index] = self.null_text

    def delete_comment(self):
        self._isComment = False
        self.comment = ''

    def save(self):
        lines = []

        if self._isComment:
            lines.append(self.comment + '\n' + self.comment_finisher)

        h_line = ''
        for h in self.headers:
            if h_line == '':
                h_line = h
            else:
                h_line += ',' + h
        lines.append(h_line)

        for i in range(len(self.columns[0])):
            line = ''

            for j in range(len(self.headers)):
                if line == '':
                    line = self.columns[j][i].replace(',', self.separator_equivalent)
                else:
                    line += ',' + self.columns[j][i].replace(',', self.separator_equivalent)

            lines.append(line)

        with open(self.path, 'w') as f:
            flag = True

            for l in lines:
                if flag:
                    flag = False
                else:
                    f.write('\n')

                f.write(l)

