from data_comm import data_writer

csv = data_writer()

csv.upload('test.csv', True)
csv.delete_comment()
csv.save()