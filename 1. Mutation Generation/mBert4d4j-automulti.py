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
import shutil
from traceback import print_exc
# import pandas as pd
locka = threading.Lock()
# from email_tool import send_email

# def get_src_file_path(project_id, version_id,repository_path=None, version_suffix=None):

#     if repository_path is None:
#         repository_path = "/home/rs/Work/Projects/D4JClean/d4jclean"

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

def get_file_lines(file_path):
    with open(file_path, 'r') as f:
        lines = sum(1 for line in f)
    return lines

def mBert4FILE(source_file_name, line_to_mutate, mutants_directory, max_num_of_mutants=None, method_name=None):
    if max_num_of_mutants is None:
        max_num_of_mutants = 100
    Path(mutants_directory).mkdir(parents=True, exist_ok=True) # /home/mutantFaultyFile/Chart/chart_1_buggy/source/org/jfree/chart/renderer/category/AbstractCategoryItemRenderer/17
    if method_name is None:
        mBert_command = ["bash", "./mBERT.sh", "-in={}".format(source_file_name), "-out={}".format(mutants_directory), "-N={}".format(max_num_of_mutants), "-l={}".format(line_to_mutate)]
        # p = subprocess.Popen(mBert_command, cwd="/home/rs/Work/Projects/SoftwareTesting/Mutation/NeuralMutation/mbert/MutationTool/mBERT", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # psutil.Process(p.pid).nice(5)
        # p.wait()
        # return p.returncode
        # 这个函数用 subprocess 来执行一个名为 mBERT.sh 的 Bash 脚本。可能是为了软件测试或其他目的。这里的命令包括了一系列的参数，如输入文件、输出目录、变异体数量和要变异的行号。
        mutate_flag = subprocess.run(mBert_command, cwd="/home/rs/Work/Projects/SoftwareTesting/Mutation/NeuralMutation/mbert/MutationTool/mBERT", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # CompletedProcess(args=['bash', './mBERT.sh', '-in=/home/rs/Work/Projects/D4JClean/d4jclean/Chart/1b/source/org/jfree/chart/renderer/category/AbstractCategoryItemRenderer.java', '-out=/home/mutantFaultyFile/Chart/chart_1_buggy/source/org/jfree/chart/renderer/category/AbstractCategoryItemRenderer/12', '-N=100', '-l=12'], returncode=0) 
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
#         # process = subprocess.Popen(mBert_command, cwd="/home/rs/Work/Projects/SoftwareTesting/Mutation/NeuralMutation/mbert/MutationTool/mBERT", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         # return_code = process.returncode
#         # return return_code

#         mBert_command = ["bash", "./mBERT.sh", "-in={}".format(source_file_name), "-out={}".format(mutants_directory), "-N={}".format(max_num_of_mutants), "-l={}".format(line_to_mutate)]
#         mutate_flag = subprocess.run(mBert_command, cwd="/home/rs/Work/Projects/SoftwareTesting/Mutation/NeuralMutation/mbert/MutationTool/mBERT", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         # mutate_flag = subprocess.run(mBert_command, cwd="/home/rs/Work/Projects/SoftwareTesting/Mutation/NeuralMutation/mbert/MutationTool/mBERT")
#         # if mutate_flag.returncode == 0:
#         #     return True
#         # else:
#         #     return False
#         # return mutate_flag
#         return mutate_flag.returncode
    # if method_name is None:
    #     mBert_command = "cd /home/rs/Work/Projects/SoftwareTesting/Mutation/NeuralMutation/mbert/MutationTool/mBERT && bash ./mBERT.sh -in={} -out={} -N={} -l={} $1>/dev/null 2>&1".format(
    #     #mBert_command = "cd /home/rs/Work/Projects/SoftwareTesting/Mutation/NeuralMutation/mbert/MutationTool/mBERT && bash ./mBERT.sh -in={} -out={} -N={} -l={}".format(
    #         source_file_name,
    #         mutants_directory,
    #         max_num_of_mutants,
    #         line_to_mutate
    #     )
    #     #print(source_file_name)
    #     #print(mBert_command) # Debug
    #     mutate_flag = os.system(mBert_command)
    #     return mutate_flag


project_data_path = "/home/d4jcover"
project_clean_path = "/home/rs/Work/Projects/SoftwareTesting/DataSet/Defects4J/D4JClean/d4jclean"
faulty_file_path = "/home/rs/Work/Projects/SoftwareTesting/DataSet/Defects4J/D4JClean/faultyFile" # 每个项目各个版本的错误文件的位置
project_mutant_repository_path = "/home/rs/Work/Projects/Z-Code4Others/mbertMutantFaultyFile" # 生成变异体后的Java文件存储位置以及日志记录文件
# if not os.path.exists(project_mutant_repository_path):
#     os.makedirs(project_mutant_repository_path)
Path(project_mutant_repository_path).mkdir(parents=True, exist_ok=True)
version_suffix = "b"

'''
project:chart,    version:1b,
code_scope:每个版本所有的错误文件：
    "Chart-14": [
        "/source/org/jfree/chart/plot/CategoryPlot.java",
        "/source/org/jfree/chart/plot/XYPlot.java"
    ],
'''
def getMutant(projectList, versionList, process_name):
    for project_id in projectList:
        for version_id in versionList:
            # project_version_mutant_repository = os.path.join(project_mutant_repository_path, project_id, project_id.lower() + "_" + version_id + "_" + "buggy" if version_suffix == "b" else "fixed")
            project_version_mutant_repository = f"{project_mutant_repository_path}/{project_id}/{project_id.lower()}_{version_id}_{'buggy' if version_suffix == 'b' else 'fixed'}"  # defetcts4J-buggy文件的位置：# /home/mutantFaultyFile/Chart/chart_1_buggy
            Path(project_version_mutant_repository).mkdir(parents=True, exist_ok=True) # 创建目录，如果存在则不创建，如果需要还会创建父级目录

            # 初始化记录文件
            log_file_path = f"{project_version_mutant_repository}/mutate_log.txt"
            if not os.path.exists(log_file_path):
                with open(log_file_path, "w") as log_file:
                    json.dump(
                        {
                            "time_cost": 0,
                            "mutant_generation_info": {},
                            "mutate_percentage": {}
                        }, 
                        log_file
                    )
            
            with open(log_file_path, "r") as log_file:
                log_data = json.load(log_file)
            time_cost = log_data["time_cost"]
            mutant_generation_info = log_data["mutant_generation_info"]
            mutate_percentage = log_data["mutate_percentage"]

            try:
                with open(f"{faulty_file_path}/{project_id}.json", "r") as f:  # 读取记录项目错误文件的json文件：/home/faultyFile/Chart.json
                    code_scope = json.load(f)[f"{project_id}-{version_id}"]
                # code_scope = pd.read_csv(
                #     os.path.join(
                #         project_data_path, 
                #         project_id,
                #         "{}_{}_code_entity_scope.csv".format(project_id, version_id + version_suffix)
                #     )
                # )
                # code_scope = pd.read_csv(
                #     f"{project_data_path}/{project_id}/{project_id}_{version_id}{version_suffix}_code_entity_scope.csv"
                # )
            except FileNotFoundError:
                print("FileNotFoundError 文件没有找到")
                continue
            
            # log init
            try:
                log_file_name = f"{project_version_mutant_repository}/{project_id}_{version_id}{version_suffix}_mutate_log.txt" # /home/mutantFaultyFile/Chart/chart_1_buggy_mutate_log.txt
                locka.acquire()
                fp = open(log_file_name, mode="a+", encoding="UTF-8")
                fp.write("")
                fp.close()
                # log_file_name = os.path.join(
                #     project_version_mutant_repository,
                #     "{}_{}_mutate_log.txt".format(project_id, version_id + version_suffix)
                # )
            finally:
                locka.release()
            # mutate
            # code_scope = code_scope[code_scope["class"].isnull()]
            # src_file_path = get_src_file_path(project_id, version_id)
            # for i in code_scope.index[0:1]: # Debug
            # for i in code_scope.index:
            for i in code_scope:  # 遍历项目的每个版本例如"Chart-1": ["/source/org/jfree/chart/renderer/category/AbstractCategoryItemRenderer.java"],
                # src = code_scope.loc[i,"src"]
                src = i
                # if project_id == 'Time' and str(version_id) == '1':
                #     src = 'org/joda' + src
                # source_file_name = os.path.join(src_file_path, src.replace(".","/") + ".java")
                # source_file_name = os.path.join(src_file_path, src)
                # source_file_name = Path(src_file_path) / src
                # source_file_name = f"{src_file_path}/{src}"
                source_file_name = f"{project_clean_path}/{project_id}/{version_id}b{src}" # 获取错误的源Java文件：/home/rs/Work/Projects/D4JClean/d4jclean/chart/1b/source/org/jfree/chart/renderer/category/AbstractCategoryItemRenderer.java
                # line_to_mutate = code_scope.loc[i, "line"] + 1
                lines_num = get_file_lines(source_file_name) # 获取该文件的所有行数
                for line_to_mutate in range(1, lines_num + 1): # 遍历错误文件的每一行，行号 ps:含头不含尾
                    mutants_directory = f"{project_version_mutant_repository}{src[:-5]}/{line_to_mutate}" # /home/mutantFaultyFile/Chart/chart_1_buggy/source/org/jfree/chart/renderer/category/AbstractCategoryItemRenderer/17 
                    if f"{project_version_mutant_repository}{src[:-5]}" not in mutant_generation_info.keys():
                        mutant_generation_info[f"{project_version_mutant_repository}{src[:-5]}"] = []
                        mutate_percentage[f"{project_version_mutant_repository}{src[:-5]}"] = "0%"

                    if f"{line_to_mutate}" in mutant_generation_info[f"{project_version_mutant_repository}{src[:-5]}"]:
                        print(f"-------------跳过！已经完成生成{project_id}-{version_id}-{line_to_mutate}---------------")
                        continue
                    else:
                        if os.path.exists(mutants_directory):
                            shutil.rmtree(mutants_directory)
                        print(f"-------------开始变异{project_id}-{version_id}-行号-{line_to_mutate}---------------")

                    
                    time_start=time.time()
                    mutate_flag = mBert4FILE(
                        source_file_name=source_file_name, 
                        line_to_mutate=line_to_mutate,
                        mutants_directory=mutants_directory,
                    )
                    # 记录下面的日志
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
                    # pdb.set_trace()

                    time_cost += time_end - time_start
                    mutant_generation_info[f"{project_version_mutant_repository}{src[:-5]}"].append(f"{line_to_mutate}")
                    mutate_percentage[f"{project_version_mutant_repository}{src[:-5]}"] = "{:.2f}%".format(
                        len(mutant_generation_info[f"{project_version_mutant_repository}{src[:-5]}"])/lines_num*100
                    )

                    with open(log_file_path, "w") as log_file:
                        json.dump(
                            {
                                "time_cost": time_cost,
                                "mutant_generation_info": mutant_generation_info,
                                "mutate_percentage": mutate_percentage
                            }, 
                            log_file
                        )
            
    # send_email(receiver='byragon@foxmail.com', subject="{}-{} 执行完成 148服务器".format(projectList[0], process_name), mail_msg='内容')


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

def startProcess(projectList, svid, evid, num_threads = 10):
    num_threads = num_threads  # Specify the number of threads you want to use
    total_versions = evid - svid + 1
    len1 = math.ceil(total_versions / num_threads)
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
        versionLists[thread_no].append(str(version))

    print(versionLists)

    # Create a process pool with specified number of workers
    with ProcessPoolExecutor(max_workers=num_threads) as pool:
        # Submit the jobs to the pool
        futures = [pool.submit(getMutant, projectList, versionList, f'process{index}') for index, versionList in enumerate(versionLists)]
        # Wait for all the jobs to complete
        for future in futures:
            future.result()

if __name__ == '__main__':
    '''
        Compress:47,Math:106,Time:27,Lang:65,Jsoup:93,Mockito:38,Codec:18,Chart:26,Closure:176
        JacksonCore:26,JacksonXml:6,Gson:18,Csv:16,Codec:18,Cli:39,
    '''
    # startProcess(["JacksonXml"], 1, 6,num_threads=10)
    # startProcess(["Gson"], 1, 18,num_threads=10)
    # startProcess(["Csv"], 1, 16,num_threads=10)
    # startProcess(["Codec"], 1, 18,num_threads=10)
    startProcess(["JacksonCore"], 21, 26,num_threads=6)
    # startProcess(["Cli"], 1, 39,num_threads=15)
    # 1-26, 27-52, 53-72 
    # 73-96 追加了新的日志记录方式，重新运行之前的代码会重新生成！
    # startProcess(["Closure"], 73, 96, num_threads=2)
    # startProcess(["Closure"], 1, 26, num_threads=20)
    # startProcess(["Closure"], 27, 52)
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
