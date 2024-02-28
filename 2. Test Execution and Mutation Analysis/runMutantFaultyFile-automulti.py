import math
import os
import subprocess
import signal
import threading
import logging
import shutil
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import pdb
import json
# from email_tool import send_email

# 创建锁对象
lock = threading.Lock()

#设置日志文件
def setup_log(adr):
    # 配置日志输出位置和级别
    logging.basicConfig(filename=adr, level=logging.DEBUG)
# def setup_log(pid, vid):
#     # 先关闭之前的日志记录器实例
#     logging.shutdown()

#     # 设置日志文件路径
#     adr = "/home/mutantlog/{}/{}-{}.log".format(pid, pid, vid)

#     # 如果日志文件夹不存在则创建
#     log_dir = os.path.dirname(adr)
#     if not os.path.exists(log_dir):
#         os.makedirs(log_dir)

#     # 配置日志输出位置和级别
#     logging.basicConfig(filename=adr, level=logging.DEBUG)

    
#创建多线程文件夹
def mkFile(runMutantPath, project, version):
  for i in range(3):
    targetFile = runMutantPath + '/' + project + '/' + version + 'b/' + str(i)
    if not os.path.exists(targetFile):
      os.makedirs(targetFile)
  return runMutantPath + '/' + project + '/' + version + 'b/'

#为目标文件夹转移文件
def copyInitFile(initPath, targetPath):
  for i in range(3):
    tmptargetPath = targetPath + str(i)
    copyCode = "cp -r {} {}".format(initPath, tmptargetPath)
    copyCodeFlag = os.system(copyCode)
    if (copyCodeFlag):
      print('复制到{}失败'.format(tmptargetPath))
    else:
      print('复制到{}完成'.format(tmptargetPath))

#均分变异体
def split_list(lst, n):
    length = len(lst)
    step = math.ceil(length / n)
    return [lst[i:i+step] for i in range(0, length, step)]

#整理变异体位置
def findMutant(mutantPath):
  search_path = mutantPath
  file_list = []

  find_command = f"find {search_path} -type f -name '*.java'"

  result = subprocess.run(find_command, shell=True, stdout=subprocess.PIPE)

  for file in result.stdout.decode().split('\n'):
      if file:
          file_list.append(file)

  # print(file_list)
  return file_list
  # return split_list(file_list, 3)

#文件备份 在clean版本的源错误java文件旁边备份一份bak文件
def backup_file(file_path):
  try:
    shutil.copy(file_path, file_path + '.bak')
    # print("{} 文件备份成功!".format(file_path))
    with lock:
      logging.info("{} 文件备份成功！".format(file_path))
  except IOError as e:
    # print("{} 文件备份失败: ".format(file_path), e)
    with lock:
      logging.error("{} 文件备份失败：{}".format(file_path, e))

#文件替换，将变异后的错误文件，替换到clean版本项目下
def replace_file(src, dst):
  try:
    shutil.copy(src, dst)
    # print("{} 替换为 {} 成功！".format(dst, src))
    with lock:
      logging.info("{} 替换为 {} 成功！".format(dst, src))
  except IOError as e:
    # print("{} 替换为 {} 失败！".format(dst, src), e)
    with lock:
      logging.error("{} 替换为 {} 失败！{}".format(dst, src, e))

#文件还原并删除，将bak后缀的源clean版本Java文件替换为原来的临时替换的文件
def restore_file(file_path):
  bak_file_path = file_path + ".bak"
  if os.path.exists(bak_file_path):
    try:
        # 使用shutil模块中的move()函数来还原备份文件
        shutil.move(bak_file_path, file_path)
        # print('{} 还原成功'.format(file_path))
        with lock:
          logging.info('{} 还原成功'.format(file_path))
        return True
    except Exception as e:
        # print('{} 还原失败'.format(file_path), e)
        with lock:
          logging.error('{} 还原失败'.format(file_path), e)
        return False
  else:
      print('备份文件不存在')
      return False
  
#执行测试
def run_d4j_test(run_path, process_name):
    # 构造命令行参数
    cmd = ["defects4j", "test", "-w", run_path, "$1>/dev/null", "2>&1"]
    # 设置超时时间
    timeout_seconds = 300
    # 调用subprocess.Popen()函数创建子进程执行命令
    try:
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, preexec_fn=os.setsid) as proc:
            try:
                stdout, stderr = proc.communicate(timeout=timeout_seconds)
            except subprocess.TimeoutExpired:
                print("{} 执行测试超时 {}".format(run_path, process_name))
                with lock:
                    logging.error("{} 执行测试超时 {}".format(run_path, process_name))
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM) # 强制杀死子进程
                return False
            if proc.returncode == 0:
                print("{} 执行测试成功 {}".format(run_path, process_name))
                with lock:
                    logging.info("{} 执行测试成功 {}".format(run_path, process_name))
                    # logging.info("输出信息：{}".format(stdout))
                return True
            else:
                print("{} 执行测试失败 {}".format(run_path, process_name))
                with lock:
                    logging.error("{} 执行测试失败 {}".format(run_path, process_name))
                    # logging.error("错误信息：{}".format(stderr))
                return False
    except subprocess.CalledProcessError as e:
        print("{} 执行测试失败".format(run_path))
        with lock:
            logging.error("{} 执行测试失败".format(run_path))
            logging.error("错误信息：{}".format(e.stderr.decode()))
        return False


#转储结果文件
def saveResult(runPath, mutantTestResultPath, target_file_name):
    failtxt = os.path.join(
        runPath,
        "failing_tests"
    )
    targetfailtxt = os.path.join(
        mutantTestResultPath + '/',
        "{}".format(target_file_name)
    )
    try:
        shutil.move(failtxt, targetfailtxt)
        # print("{} 转储 {} 成功".format(failtxt, target_file_name))
        with lock:
           logging.info("{} 转储 {} 成功\n------".format(failtxt, target_file_name))
    except Exception as e:
        # print("{} 转储 {} 失败: {}".format(failtxt, target_file_name, e))
        with lock:
           logging.error("{} 转储 {} 失败: {}\n------".format(failtxt, target_file_name, e))

#获取d4j源目录
def get_src_file_path(pid, vid, repository_path=None, version_suffix=None):

    if repository_path is None:
        # repository_path = "/home/runmutant/Chart/2b"
        repository_path = "/home/rs/Work/Projects/SoftwareTesting/DataSet/Defects4J/D4JClean/d4jclean/" + pid + "/" + vid + "b"

    if version_suffix is None:
        version_suffix = "b"

    # obtain the source code folder
    # project_path = "{}/{}/{}".format(
    #     repository_path,
    #     index,
    #     pid + "-" + vid + "b"
    # )
    # d4j_export_command = "cd {} && defects4j export -p dir.src.classes".format(repository_path)
    # dir_src_classes = os.popen(d4j_export_command).read()
    d4j_export_command = ["defects4j", "export", "-p", "dir.src.classes", "$1>/dev/null", "2>&1"]
    # dir_src_classes = subprocess.check_output(d4j_export_command, cwd=repository_path).decode().strip()
    dir_src_classes = subprocess.check_output(d4j_export_command, cwd=repository_path, stderr=subprocess.DEVNULL).decode().strip()
    src_file_path = "{}/{}".format(
        repository_path,
        dir_src_classes,
    )
   # print("源路径为{}".format(dir_src_classes))
    return src_file_path
# 获取
def getRunMutantLog(pid,vid):
  runMutantLog_path = f"/home/rs/Work/Projects/Z-Code4Others/runMutantLog/{pid}/{pid}-{vid}.json"
  os.makedirs(os.path.dirname(runMutantLog_path), exist_ok=True)
  # 检查文件是否存在，如果不存在，创建一个空的json文件
  if not os.path.exists(runMutantLog_path):
    with open(runMutantLog_path, 'w', encoding='utf-8') as file:
      # 需要更新下数据结构:
      json.dump({
         "mutantRecord":{},
         "success_mutant_num":{}
      }, file) # 创建一个空字典或者任何初始结构
  with open(runMutantLog_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
    return data
def writeRunMutantLog(pid,vid,data):
  runMutantLog_path = f"/home/rs/Work/Projects/Z-Code4Others/runMutantLog/{pid}/{pid}-{vid}.json"
  os.makedirs(os.path.dirname(runMutantLog_path), exist_ok=True)
  with open(runMutantLog_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

#执行变异体 pid, versionList[str(i)], 'process%d'%(i,)
def execMutant(pid, mutantPath, process_name): # ['/home/rs/Work/Projects/Z-Code4Others/mbertMutantFaultyFile/Closure/closure_28_buggy', '/home/rs/Work/Projects/Z-Code4Others/mbertMutantFaultyFile/Closure/closure_29_buggy']
  for i in mutantPath:
    mutantList = findMutant(i) # ['/home/rs/Work/Projects/Z-Code4Others/mbertMutantFaultyFile/Closure/closure_27_buggy/src/com/google/javascript/rhino/IR/263/6/IR.java', '/home/rs/Work/Projects/Z-Code4Others/mbertMutantFaultyFile/Closure/closure_27_buggy/src/com/google/javascript/rhino/IR/263/0/IR.java']
    vid = i.split("_")[1]
    adr = "/home/rs/Work/Projects/Z-Code4Others/mutantlog_faulty_file/{}/{}-{}.log".format(pid, pid, vid) # 日志的位置
    if not os.path.exists(os.path.dirname(adr)):
        os.makedirs(os.path.dirname(adr))
    setup_log(adr)
    runMutantLog = getRunMutantLog(pid,vid)
    # success_mutant_num = getRunMutantLog(pid,vid) # 记录当前行成功执行的变异体数量，需要替换成从文件读取，建议以版本粒度存取
    for item in mutantList:
      file_path = item # /home/rs/Work/Projects/Z-Code4Others/mbertMutantFaultyFile/Closure/closure_27_buggy/src/com/google/javascript/rhino/IR/101/7/IR.java,
      sourceFilePath = "/home/rs/Work/Projects/SoftwareTesting/DataSet/Defects4J/D4JClean/d4jclean/" + pid + "/" + vid + "b/" # clean项目的头路径
      new_path = '/'.join(file_path.split('/')[10:-3]) # src/com/google/javascript/jscomp/InlineCostEstimator
      target_path = sourceFilePath + new_path + '.java' # 目标错误文件的位置 /home/rs/Work/Projects/SoftwareTesting/DataSet/Defects4J/D4JClean/d4jclean/Closure/28b/src/com/google/javascript/jscomp/InlineCostEstimator.java
      target_file_name = '/'.join(file_path.split('/')[10:-1])
      target_file_name = target_file_name.replace('/', '-') # /home/rs/Work/Projects/SoftwareTesting/DataSet/Defects4J/D4JClean/d4jclean/Closure/27b/src/com/google/javascript/rhino/IR.java,
      runPath = "/home/rs/Work/Projects/SoftwareTesting/DataSet/Defects4J/D4JClean/d4jclean/{}/{}b".format(pid, vid) # /home/rs/Work/Projects/SoftwareTesting/DataSet/Defects4J/D4JClean/d4jclean/Closure/27b
      mutantLine = '-'.join(target_file_name.split('-')[:-1]) # src-com-google-javascript-rhino-IR-101 # 记录了一些信息
      # 创建一个记录成功执行的变异体的文件，一个项目一个文件
      # pdb.set_trace()
      if file_path in runMutantLog["mutantRecord"]:
        print("------------已经执行过变异体项目:"+file_path+"-------------------")
        continue
      if mutantLine in runMutantLog["success_mutant_num"] and runMutantLog["success_mutant_num"][mutantLine] >= 3: #>=3的原因是
        print("------------该行变异体succ超过3:"+mutantLine+"-------------------")
        continue
      backup_file(target_path) # 文件备份，将原来的clean的java文件备份一份
      replace_file(file_path, target_path) # 替换文件为变异后的错误文件
      runresult = run_d4j_test(runPath, process_name) # 执行测试
      str = f"----------变异执行完成:{mutantLine}-runresult为:{runresult}---------"
      print(str)
      restore_file(target_path) # 把原来的文件替换回来
      runMutantLog["mutantRecord"][file_path] = runresult # 表示该变异体已经执行过了
      if runresult: # 执行成功
        if mutantLine not in runMutantLog["success_mutant_num"]: # 需要改成替换文件
          runMutantLog["success_mutant_num"][mutantLine] = 1
        else:
          runMutantLog["success_mutant_num"][mutantLine] += 1
        # mutantTestResultPath = "/home/mutant_result/{}/{}b".format(pid, vid)
        mutantTestResultPath = "/home/rs/Work/Projects/Z-Code4Others/mutant_result_faulty_file/{}/{}b".format(pid, vid)
        if not os.path.exists(mutantTestResultPath):
          os.makedirs(mutantTestResultPath)
        saveResult(runPath, mutantTestResultPath, target_file_name)
      writeRunMutantLog(pid,vid,runMutantLog) # 写入文件中，防止程序异常关闭success_mutant_num消失
  # try:
  #   send_email(receiver='changzexing687@163.com', subject="{}-{} 执行完成 148服务器".format(pid, process_name), mail_msg='内容')
  #   print(f"{process_name} 发送成功")
  # except:
  #   print(f"{process_name} 发送失败")

  
#开始多线程
def startThread(mutantPath, pid, svid, evid):
  len = (evid - svid + 1) // 3
  versionList0 = []
  versionList1 = []
  versionList2 = []
  for i in range(svid, svid + len):
    if str(i) == '2':
       continue
    versionList0.append(mutantPath + pid + "/" + str(pid).lower() + "_" + str(i) + "_buggy")
  for i in range(svid + len, evid + 1):
    if str(i) == '2':
       continue
    versionList1.append(mutantPath + pid + "/" + str(pid).lower() + "_" + str(i) + "_buggy")
  for i in range(svid + 2 * len, evid + 1):
    if str(i) == '21':
       continue
    versionList2.append(mutantPath + pid + "/" + str(pid).lower() + "_" + str(i) + "_buggy")
  versionList = {}
  versionList['0'] = versionList0
  # execMutant(pid, versionList0, "0")
  versionList['1'] = versionList1
  versionList['2'] = versionList2
  # print(versionList)
  # parts = findMutant(mutantPath)
  # sourceFilePath = get_src_file_path(project, version) + '/'
  threads = [threading.Thread(name='t%d'%(i,), target=execMutant, args=(pid, versionList[str(i)], )) for i in range(3)]
  [t.start() for t in threads]

#初始化
def initProgram(runMutantPath, project, version, initPath):
  targetPath = mkFile(runMutantPath, project, version)
  copyInitFile(initPath, targetPath)

#开始多进程,传入mutantPath：/home/rs/Work/Projects/Z-Code4Others/mbertMutantFaultyFile/      
def startProcess(mutantPath, pid, svid, evid, num_threads = 6):
    num_threads = num_threads  # Specify the number of threads you want to use
    total_versions = evid - svid + 1
    len1 = math.ceil(total_versions // num_threads)
    versionLists = [[] for _ in range(num_threads)]  # Create a list of lists for version numbers
    No = set()  # Use a set for faster lookups

    # Divide versions among threads
    for i in range(total_versions):
        version = svid + i
        if str(version) in No:
            continue
        thread_no = i // len1  # Determine which thread this version belongs to
        if thread_no >= num_threads:  # Ensure thread_no doesn't exceed the number of threads
            thread_no = num_threads - 1
        versionLists[thread_no].append(mutantPath + pid + "/" + str(pid).lower() + "_" + str(version) + "_buggy")

    for index, versionList in enumerate(versionLists):
      print(index, versionList, len(versionList))

    # Create a process pool with specified number of workers
    with ProcessPoolExecutor(max_workers=num_threads) as pool:
        # Submit the jobs to the pool
        futures = [pool.submit(execMutant, pid, versionList, f'process{index}') for index, versionList in enumerate(versionLists)]
        # Wait for all the jobs to complete
        for future in futures:
            future.result()


if __name__ == '__main__':
  # initProgram("./runmutant", "Chart", "1", "./getLang.py")
  # initProgram("/home/runmutant", "Chart", "1", "/home/rs/Work/Projects/SoftwareTesting/DataSet/Defects4J/D4JClean/d4jcleanChart/1b/")
  # execMutant("/home/mutant/Chart/chart_1_buggy")
  # startThread("/home/mutant/", "Time", 1, 27)
  # startThread("/home/mutant/", "Lang", 1, 65)
  # 采取中间文件的目的是防止clean版本的某个文件替换为变异体的文件时，程序停止执行了，这样子clean版本就会发生变化，所以找一个中间文件tmp
  # cp clean复制到tmp，复制之前要处理tmp文件夹的问题，方案1，cp前删掉tmp；方案2：执行cp 命令时采取新文件覆盖旧文件的指令
  # 由于把clean的执行改到了tmp，所以上面clean的路径要替换成tmp的
  # startProcess("/home/rs/Work/Projects/Z-Code4Others/mbertMutantFaultyFile/", "Closure", 1, 27, num_threads=9)
  # startProcess("/home/rs/Work/Projects/Z-Code4Others/mbertMutantFaultyFile/", "Mockito", 1, 32, num_threads=8)
  # startProcess("/home/rs/Work/Projects/Z-Code4Others/mbertMutantFaultyFile/", "Closure", 73, 96, num_threads=8)
  # startProcess("/home/rs/Work/Projects/Z-Code4Others/mbertMutantFaultyFile/", "Closure", 53, 72, num_threads=10)
  # startProcess("/home/rs/Work/Projects/Z-Code4Others/mbertMutantFaultyFile/", "Closure", 97, 133, num_threads=12)
  # startProcess("/home/rs/Work/Projects/Z-Code4Others/mbertMutantFaultyFile/", "JacksonXml", 1, 6, num_threads=6)
  # startProcess("/home/rs/Work/Projects/Z-Code4Others/mbertMutantFaultyFile/", "Gson", 1, 18, num_threads=18)
  # startProcess("/home/rs/Work/Projects/Z-Code4Others/mbertMutantFaultyFile/", "Csv", 1, 16, num_threads=16)  
  startProcess("/home/rs/Work/Projects/Z-Code4Others/mbertMutantFaultyFile/", "JacksonCore", 21, 26, num_threads=6)
  # startProcess("/home/mutantFaultyFile/", "Lang", 1, 65)
  # startProcess("/home/zuhemutantSFClu/", "Chart", 1, 26)
  # startProcess("/home/zuhemutantSFClu/", "Time", 1, 27)
  # startProcess("/home/zuhemutantSFClu/", "Lang", 1, 65)
  # startProcess("/home/mutant/", "Csv", 1, 16)
  # startProcess("/home/mutant/", "Math", 1, 106)
  # result = os.system('ls')

  # print(result)
