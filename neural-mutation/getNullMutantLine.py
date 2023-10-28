import os


def check_file_size(file_path):
    if os.path.isfile(file_path):
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            return "Empty file"
        else:
            return file_size
    else:
        return "File does not exist"


#读取csv文件
def read_csv_file(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        # Skip header row
        next(reader, None)
        for row in reader:
            data.append(row)
    return data

#将没有变异体的行存入新的csv
def write_to_csv(filename, pid, vid, data):
    if not os.path.exists(filename):
      os.makedirs(filename)
    with open(filename + "/" "{}_{}b_code_entity_scope.csv".format(pid, vid), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['src', 'line'])  # 添加表头
        for item in data:
          writer.writerow(item)

def getMutantFileSize(mutantLineList, pid, vid):
    num = 0
    data = []
    for item in mutantLineList:
      mutantPath = "/home/changzexing/mutant/{}/{}_{}_buggy/{}/{}/map-{}.txt".format(pid, pid.lower(), vid, item[0].split('.')[0], int(item[1]) + 1, item[0].split('.')[0].split('/')[-1])
      # print(mutantPath)
      result = check_file_size(mutantPath)
      if result == "File does not exist" or result == "Empty file":
         num += 1
         data.append(item)
    csvPath = "/home/changzexing/nullMutantLine/{}".format(pid)
    write_to_csv(csvPath, pid, vid, data)
    print(num)
      # break
def init(pid, svid, evid):
    for item in range(svid, evid + 1):
      csvpath = "/home/changzexing/d4jcover/{}/{}_{}b_code_entity_scope.csv".format(pid, pid, item)
      if not os.path.exists(csvpath):
        continue
      mutantLineList = read_csv_file(csvpath)
      getMutantFileSize(mutantLineList, pid, item)
      # break

if __name__ == '__main__':
    init("Chart", 1, 26)