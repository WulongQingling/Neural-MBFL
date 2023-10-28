from email import header
import pickle
import csv
import os
from pathlib import Path

# ��ȡ���Ǿ���������ļ�
def coverInfo(coverageMatrixPath, testResult, hugToFilePath, project, version, targetSrc):
  # ��ȡ��������ִ�н��
  with open(testResult, 'rb') as tr:
    testContent = pickle.load(tr)
    # print(testContent[0], type(testContent))
  with open("./1b/faultLineSimpleIndex.in", 'rb') as ab:
    a = pickle.load(ab)
    print(a)
  # ��ȡ������Ϣ
  with open(coverageMatrixPath, 'rb') as fp:
    content = pickle.load(fp)
    for item in range(len(content)):
      if testContent[item] == 1:
        getCoverCsv(content[item], hugToFilePath, project, version, targetSrc)
    # print(len(content), len(content[0]), type(content[0][1]))

# ���ݸ�����Ϣ�ҵ���Ӧ��java�ļ�������
def getCoverCsv(coverData, hugToFilePath, project, version, targetSrc):
  header = ["src", "line"]
  my_file = Path(targetSrc + '/' + project)
  print(my_file.exists())
  if not my_file.exists():
    os.makedirs(targetSrc + '/' + project)
  csvData = open(targetSrc + '/' + project + '/' + project + '_' + version + '_code_entity_scope.csv', 'w', newline='')
  write = csv.writer(csvData)
  write.writerow(header)
  hugContent = [] # �洢����������Ϣ
  with open(hugToFilePath, 'rb') as fp:
    # flag = True
    for item in fp.readlines():
      item = str(item) # bytesתstr
      item = item.replace("b'", "").replace("'", "").replace("\\n", "").replace("\\t", "") # ֻ����src���к�
      # if flag:
      #   print(type(item), item)
      #   flag = False
      lineNum = ""
      # �����к�
      for i in item[::-1]:
        if i == "a":
          break
        lineNum = i + lineNum
      item = item.replace(lineNum, "")
      hugContent.append({'item' : item, 'lineNum' : lineNum})
      # print(hugContent[len(hugContent) - 1])
  # ����csv
  num = 0
  for val in range(len(coverData)):
    if (coverData[val] == 1):
      # print(hugContent[val])
      num+=1
      write.writerow([hugContent[val]['item'], hugContent[val]['lineNum']])
  print(num) 

if __name__ == '__main__':
  # coverInfo("./1b/CoverageMatrix.in", "./1b/inVector.in", "./1b/HugeToFile.txt", 'Chart', '1b', "d:\d4j")
  # pid = 'Csv'
  # svid = 1
  # evid = 16
  pid = 'Chart'
  svid = 1
  evid = 26
  for i in range(svid, evid + 1):
    # if str(i) == '2':
    #   continue
    if not os.path.exists("/home/changzexing/d4jbasecover/" + pid + "/" + str(i) + "b/faultLineSimpleIndex.in"):
      continue
    with open("/home/changzexing/d4jbasecover/" + pid + "/" + str(i) + "b/faultLineSimpleIndex.in", 'rb') as ab:
      a = pickle.load(ab)
      # content = "Time" + str(i) + a
      with open("/home/changzexing/faultyLine/" + pid + "FalutLine.txt", "a") as f:
        print('{} {} {}'.format(pid, str(i), a), file=f)