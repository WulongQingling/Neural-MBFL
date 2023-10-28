# Environment
# conda activate mBert
# java 11

import multiprocessing
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import os
import threading
import subprocess
import math
import time
import json
import pandas as pd
locka = threading.Lock()
# from email_tool import send_email

# def get_src_file_path(project_id, version_id,repository_path=None, version_suffix=None):

#     if repository_path is None:
#         repository_path = "/home/changzexing/d4jclean"

#     if version_suffix is None:
#         version_suffix = "b"

#     # obtain the source code folder
#     project_path = "{}/{}/{}".format(
#         repository_path,
#         project_id,
#         version_id + "b"
#     )
#     d4j_export_command = "cd {} && defects4j export -p dir.src.classes".format(project_path)
#     dir_src_classes = os.popen(d4j_export_command).read()
#     src_file_path = "{}/{}/{}/{}".format(
#         repository_path,
#         project_id,
#         version_id + "b",
#         dir_src_classes,
#     )
#     return src_file_path
def get_src_file_path(pid, vid, repository_path=None, version_suffix=None):

    if repository_path is None:
        # repository_path = "/home/changzexing/runmutant/Chart/2b"
        repository_path = "/home/changzexing/d4jclean/" + pid + "/" + vid + "b"

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

def get_file_lines(file_path):
    with open(file_path, 'r') as f:
        lines = sum(1 for line in f)
    return lines

def mBert4FILE(source_file_name, line_to_mutate, mutants_directory, max_num_of_mutants=None, method_name=None):
    if max_num_of_mutants is None:
        max_num_of_mutants = 100
    
    Path(mutants_directory).mkdir(parents=True, exist_ok=True)

    if method_name is None:
        mBert_command = ["bash", "./mBERT.sh", "-in={}".format(source_file_name), "-out={}".format(mutants_directory), "-N={}".format(max_num_of_mutants), "-l={}".format(line_to_mutate)]
        # p = subprocess.Popen(mBert_command, cwd="/home/changzexing/mbert/mBERT-main", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # psutil.Process(p.pid).nice(5)
        # p.wait()
        # return p.returncode
        mutate_flag = subprocess.run(mBert_command, cwd="/home/changzexing/mbert/mBERT-main", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return mutate_flag.returncode

# def mBert4FILE(source_file_name, line_to_mutate, mutants_directory, max_num_of_mutants=None, method_name=None):
#     if max_num_of_mutants is None:
#         max_num_of_mutants = 5
    
#     # if not os.path.exists(mutants_directory):
#     #     os.makedirs(mutants_directory)
#     Path(mutants_directory).mkdir(parents=True, exist_ok=True)

#     if method_name is None:
#         # mBert_command = ["bash", "./mBERT.sh", "-in={}".format(source_file_name), "-out={}".format(mutants_directory), "-N={}".format(max_num_of_mutants), "-l={}".format(line_to_mutate)]
#         # mBert_command = ["bash", "./mBERT.sh", "-in={}".format(source_file_name), "-out={}".format(mutants_directory), "-N={}".format(max_num_of_mutants), "-l={}".format(line_to_mutate)]
#         # process = subprocess.Popen(mBert_command, cwd="/home/changzexing/mbert/mBERT-main", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         # return_code = process.returncode
#         # return return_code

#         mBert_command = ["bash", "./mBERT.sh", "-in={}".format(source_file_name), "-out={}".format(mutants_directory), "-N={}".format(max_num_of_mutants), "-l={}".format(line_to_mutate)]
#         mutate_flag = subprocess.run(mBert_command, cwd="/home/changzexing/mbert/mBERT-main", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         # mutate_flag = subprocess.run(mBert_command, cwd="/home/changzexing/mbert/mBERT-main")
#         # if mutate_flag.returncode == 0:
#         #     return True
#         # else:
#         #     return False
#         # return mutate_flag
#         return mutate_flag.returncode
    # if method_name is None:
    #     mBert_command = "cd /home/changzexing/mbert/mBERT-main && bash ./mBERT.sh -in={} -out={} -N={} -l={} $1>/dev/null 2>&1".format(
    #     #mBert_command = "cd /home/changzexing/mbert/mBERT-main && bash ./mBERT.sh -in={} -out={} -N={} -l={}".format(
    #         source_file_name,
    #         mutants_directory,
    #         max_num_of_mutants,
    #         line_to_mutate
    #     )
    #     #print(source_file_name)
    #     #print(mBert_command) # Debug
    #     mutate_flag = os.system(mBert_command)
    #     return mutate_flag




project_data_path = "/home/changzexing/d4jcover"
project_clean_path = "/home/changzexing/d4jclean"
faulty_file_path = "/home/changzexing/faultyFile"
project_mutant_repository_path = "/home/changzexing/mutantFaultyFile"
# if not os.path.exists(project_mutant_repository_path):
#     os.makedirs(project_mutant_repository_path)
Path(project_mutant_repository_path).mkdir(parents=True, exist_ok=True)
version_suffix = "b"

def getMutant(projectList, versionList, process_name):
    # print('开始执行', projectList, versionList)
    for project_id in projectList:
        for version_id in versionList:
            time_start=time.time()
            # print(threading.current_thread().getName())
            # ensure the project version mutant repository
            # project_version_mutant_repository = os.path.join(project_mutant_repository_path, project_id, project_id.lower() + "_" + version_id + "_" + "buggy" if version_suffix == "b" else "fixed")
            project_version_mutant_repository = f"{project_mutant_repository_path}/{project_id}/{project_id.lower()}_{version_id}_{'buggy' if version_suffix == 'b' else 'fixed'}"

            # if not os.path.exists(project_version_mutant_repository):
            #     os.makedirs(project_version_mutant_repository)
            Path(project_version_mutant_repository).mkdir(parents=True, exist_ok=True)
            # print(project_version_mutant_repository)
            # print(project_id, version_id + version_suffix)
            try:
                # code_scope = pd.read_csv(
                #     os.path.join(
                #         project_data_path, 
                #         project_id,
                #         "{}_{}_code_entity_scope.csv".format(project_id, version_id + version_suffix)
                #     )
                # )
                # print(f"{faulty_file_path}/{project_id}.json")
                with open(f"{faulty_file_path}/{project_id}.json", "r") as f:
                    # 读取json文件
                    code_scope = json.load(f)[f"{project_id}-{version_id}"]
                    # print(code_scope, "ss")
                # code_scope = pd.read_csv(
                #     f"{project_data_path}/{project_id}/{project_id}_{version_id}{version_suffix}_code_entity_scope.csv"
                # )

            except FileNotFoundError:
                continue
            
            # log init
            try:
                # log_file_name = os.path.join(
                #     project_version_mutant_repository,
                #     "{}_{}_mutate_log.txt".format(project_id, version_id + version_suffix)
                # )
                log_file_name = f"{project_version_mutant_repository}/{project_id}_{version_id}{version_suffix}_mutate_log.txt"

                locka.acquire()
                fp = open(log_file_name, mode="a+", encoding="UTF-8")
                fp.write("")
                fp.close()
            finally:
                locka.release()
            # mutate
            # code_scope = code_scope[code_scope["class"].isnull()]
            # src_file_path = get_src_file_path(project_id, version_id)
            # for i in code_scope.index[0:1]: # Debug
            # for i in code_scope.index:
            for i in code_scope:
                # src = code_scope.loc[i,"src"]
                src = i
                # if project_id == 'Time' and str(version_id) == '1':
                #     src = 'org/joda' + src
                # source_file_name = os.path.join(src_file_path, src.replace(".","/") + ".java")
                # source_file_name = os.path.join(src_file_path, src)
                # source_file_name = Path(src_file_path) / src
                # source_file_name = f"{src_file_path}/{src}"
                source_file_name = f"{project_clean_path}/{project_id}/{version_id}b{src}"
                # line_to_mutate = code_scope.loc[i, "line"] + 1
                lines_num = get_file_lines(source_file_name)
                # print(source_file_name, lines_num)
                for line_item in range(0, lines_num):
                    line_to_mutate = line_item + 1
                    mutants_directory = f"{project_version_mutant_repository}{src[:-5]}/{line_to_mutate}"
                    # print(mutants_directory)
                    mutate_flag = mBert4FILE(
                        source_file_name=source_file_name, 
                        line_to_mutate=line_to_mutate,
                        mutants_directory=mutants_directory,
                    )
                    try:
                        locka.acquire()
                        fp = open(log_file_name, mode="a+", encoding="UTF-8")
                        fp.write("{} : line {} : {} Use jincheng {}\n".format(src, line_to_mutate, "PASS" if mutate_flag == 0 else "ERROR", process_name))
                        fp.close()
                    finally:
                        locka.release()
                        print("{} : line {} : {} Use jincheng {}".format(src, line_to_mutate, "PASS" if mutate_flag == 0 else "ERROR", process_name))
                    time_end=time.time()
                    try:
                        locka.acquire()
                        fp = open(log_file_name, mode="a+", encoding="UTF-8")
                        fp.write("Mutate {}-{}-{} Over! Use jincheng{} [time cost:{:.2f}]\n".format(project_id, version_id, src, process_name, time_end-time_start))
                        fp.write("-"*50 + "\n")
                        fp.close()
                    finally:
                        locka.release()
                        print("Mutate {}-{}-{} Over! Use jincheng{} [time cost:{:.2f}]".format(project_id, version_id, src, process_name, time_end-time_start))
                        print("-"*50 + "\n")
    # send_email(receiver='changzexing687@163.com', subject="{}-{} 执行完成 148服务器".format(projectList[0], process_name), mail_msg='内容')


def testThread(a, b):
    print(threading.current_thread().getName(), a)
    print(threading.current_thread().getName(), b)

def startThread():
    projectList = [
        "Closure"
    ]
    versionList0 = []
    versionList1 = []
    versionList2 = []
    # versionList3 = []
    for i in range(1, 24):
        versionList0.append(str(i))
    for i in range(24, 47):
        versionList1.append(str(i))
    for i in range(47, 70):
        if str(i) == 63:
            continue
        versionList2.append(str(i))
    # for i in range(48, 66):
    #     versionList3.append(str(i))
    # versionList0 = [
    #     "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25"
    # ]
    # versionList1 = ["26", "27", "28", "29", "30", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25"]
    # versionList2 = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25"]
    versionList = {}
    versionList['0'] = versionList0
    versionList['1'] = versionList1
    versionList['2'] = versionList2
    # versionList['3'] = versionList3
    # print(versionList)
    # print(versionList)
    threads = [threading.Thread(name='t%d'%(i,), target=getMutant, args=(projectList, versionList[str(i)],)) for i in range(3)]
    [t.start() for t in threads]
    # 定义进程池
    # pool = multiprocessing.Pool(processes=3)

    # # 定义进程执行的任务列表
    # task_list = [(projectList, versionList[str(i)]) for i in range(3)]

    # # 将任务列表加入进程池中
    # for task in task_list:
    #     pool.apply_async(getMutant, args=task)

    # print('关闭')
    # # 关闭进程池
    # pool.close()

    # # 等待所有进程执行完毕
    # print('加入')
    # pool.join()
    # print('?????')

def startProcess(projectList, svid, evid):
    num = 4
    len = math.ceil((evid - svid + 1) // num)
    versionList0 = []
    versionList1 = []
    versionList2 = []
    versionList3 = []
    versionList4 = []
    versionList5 = []
    No = "0" 
    for i in range(svid, svid + len):
        if str(i) == No:
            continue
        versionList0.append(str(i))

    for i in range(svid + len, svid + 2 * len):
        if str(i) == No:
            continue
        versionList1.append(str(i))

    for i in range(svid + 2 * len, svid + 3 * len):
        if str(i) == No:
            continue
        versionList2.append(str(i))

    for i in range(svid + 3 * len, evid + 1):
        if str(i) == No:
            continue
        versionList3.append(str(i))

    # for i in range(svid + 4 * len, svid + 5 * len):
    #     if str(i) == No:
    #         continue
    #     versionList4.append(str(i))

    # for i in range(svid + 5 * len, evid + 1):
    #     if str(i) == No:
    #         continue
    #     versionList5.append(str(i))

    versionList = {}
    versionList['0'] = versionList0
    versionList['1'] = versionList1
    versionList['2'] = versionList2
    versionList['3'] = versionList3
    versionList['4'] = versionList4
    versionList['5'] = versionList5

    # Create a process pool with 6 workers
    with ProcessPoolExecutor(max_workers=num) as pool:
        # Submit the jobs to the pool
        futures = [pool.submit(getMutant, projectList, versionList[str(i)], 'process%d'%(i,)) for i in range(num)]
        
        # Wait for all the jobs to complete
        for future in futures:
            future.result()

if __name__ == '__main__':
    # startProcess(["Gson"], 1, 18)
    # startProcess(["Compress"], 1, 47)
    # startProcess(["Jsoup"], 1, 93)
    # startProcess(["Math"], 1, 106)
    # startProcess(["Time"], 1, 27)
    startProcess(["Chart"], 1, 26)
    # startThread()
    # getMutant(["Chart"], ["1"])

       
# source_file_name = ""
# mutants_directory = ""
# max_num_of_mutants = ""
# line_to_mutate = ""
# method_name = None
# mBert_command = "bash /home/rs/Work/mBERT/mBERT.sh -in={} -out={} -N={} -l={}".format(
#     source_file_name,
#     mutants_directory,
#     max_num_of_mutants,
#     line_to_mutate
# )
