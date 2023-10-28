# Environment
# conda activate mBert
# java 11

import multiprocessing
import os
import threading
import time
import pandas as pd
locka = threading.Lock()

def get_src_file_path(project_id, version_id,repository_path=None, version_suffix=None):

    if repository_path is None:
        repository_path = "/home/changzexing/d4jclean"

    if version_suffix is None:
        version_suffix = "b"

    # obtain the source code folder
    project_path = "{}/{}/{}".format(
        repository_path,
        project_id,
        version_id + "b"
    )
    d4j_export_command = "cd {} && defects4j export -p dir.src.classes".format(project_path)
    dir_src_classes = os.popen(d4j_export_command).read()
    src_file_path = "{}/{}/{}/{}".format(
        repository_path,
        project_id,
        version_id + "b",
        dir_src_classes,
    )
    return src_file_path

def mBert4FILE(source_file_name, line_to_mutate, mutants_directory, max_num_of_mutants=None, method_name=None):
    if max_num_of_mutants is None:
        max_num_of_mutants = 5
    
    if not os.path.exists(mutants_directory):
        os.makedirs(mutants_directory)

    if method_name is None:
        # mBert_command = "cd /home/changzexing/mbert/mBERT-main && bash ./mBERT.sh -in={} -out={} -N={} -l={} $1>/dev/null 2>&1".format(
        mBert_command = "cd /home/changzexing/mbert/mBERT-main && bash ./mBERT.sh -in={} -out={} -N={} -l={}".format(
            source_file_name,
            mutants_directory,
            max_num_of_mutants,
            line_to_mutate
        )
        #print(source_file_name)
        #print(mBert_command) # Debug
        mutate_flag = os.system(mBert_command)
        return mutate_flag


project_data_path = "/home/changzexing/d4jcover"
project_mutant_repository_path = "/home/changzexing/mutant"
if not os.path.exists(project_mutant_repository_path):
    os.makedirs(project_mutant_repository_path)
version_suffix = "b"

def getMutant(projectList, versionList):
    for project_id in projectList:
        for version_id in versionList:
            time_start=time.time()
            # print(threading.current_thread().getName())
            # ensure the project version mutant repository
            project_version_mutant_repository = os.path.join(project_mutant_repository_path, project_id, project_id.lower() + "_" + version_id + "_" + "buggy" if version_suffix == "b" else "fixed")
            if not os.path.exists(project_version_mutant_repository):
                os.makedirs(project_version_mutant_repository)
            # print(project_version_mutant_repository)
            # print(project_id, version_id + version_suffix)
            try:
                code_scope = pd.read_csv(
                    os.path.join(
                        project_data_path, 
                        project_id,
                        "{}_{}_code_entity_scope.csv".format(project_id, version_id + version_suffix)
                    )
                )
            except FileNotFoundError:
                continue
            
            # log init
            try:
                log_file_name = os.path.join(
                    project_version_mutant_repository,
                    "{}_{}_mutate_log.txt".format(project_id, version_id + version_suffix)
                )
                locka.acquire()
                fp = open(log_file_name, mode="a+", encoding="UTF-8")
                fp.write("")
                fp.close()
            finally:
                locka.release()
            # mutate
            # code_scope = code_scope[code_scope["class"].isnull()]
            src_file_path = get_src_file_path(project_id, version_id)
            # for i in code_scope.index[0:1]: # Debug
            for i in code_scope.index:
                src = code_scope.loc[i,"src"]
                if src != '/time/Partial.java' or code_scope.loc[i, "line"] + 1 != 67:
                    continue
                if project_id == 'Time' and str(version_id) == '1':
                    src = 'org/joda' + src
                # source_file_name = os.path.join(src_file_path, src.replace(".","/") + ".java")
                source_file_name = os.path.join(src_file_path, src)
                line_to_mutate = code_scope.loc[i, "line"] + 1
                # entity_start = code_scope.loc[i, "start"]
                # entity_end = code_scope.loc[i, "end"]
                # for line_to_mutate in range(entity_start, entity_start + 1): # Debug
                # for line_to_mutate in range(entity_start, entity_end + 1):
                #     mutants_directory = os.path.join(
                #         project_version_mutant_repository,
                #         src.replace(".","/"),
                #         str(line_to_mutate)
                #     )

                #     mutate_flag = mBert4FILE(
                #         source_file_name=source_file_name, 
                #         line_to_mutate=line_to_mutate,
                #         mutants_directory=mutants_directory,
                #     )
                #     fp = open(log_file_name, mode="a", encoding="UTF-8")
                #     fp.write("{} : line {} : {}\n".format(src, line_to_mutate, "PASS" if mutate_flag == 0 else "ERROR"))
                #     fp.close()
                #     print("{} : line {} : {}".format(src, line_to_mutate, "PASS" if mutate_flag == 0 else "ERROR"))
                mutants_directory = os.path.join(
                    project_version_mutant_repository,
                    src[:-5],
                    str(line_to_mutate)
                )
                mutate_flag = mBert4FILE(
                    source_file_name=source_file_name, 
                    line_to_mutate=line_to_mutate,
                    mutants_directory=mutants_directory,
                )
                try:
                    locka.acquire()
                    fp = open(log_file_name, mode="a+", encoding="UTF-8")
                    fp.write("{} : line {} : {} Use jincheng {}\n".format(src, line_to_mutate, "PASS" if mutate_flag == 0 else "ERROR", threading.current_thread().getName()))
                    fp.close()
                finally:
                    locka.release()
                    print("{} : line {} : {} Use jincheng {}".format(src, line_to_mutate, "PASS" if mutate_flag == 0 else "ERROR", threading.current_thread().getName()))
                time_end=time.time()
                try:
                    locka.acquire()
                    fp = open(log_file_name, mode="a+", encoding="UTF-8")
                    fp.write("Mutate {}-{}-{} Over! Use jincheng{} [time cost:{:.2f}]\n".format(project_id, version_id, src, threading.current_thread().getName(), time_end-time_start))
                    fp.write("-"*50 + "\n")
                    fp.close()
                finally:
                    locka.release()
                    print("Mutate {}-{}-{} Over! Use jincheng{} [time cost:{:.2f}]".format(project_id, version_id, src, threading.current_thread().getName(), time_end-time_start))
                    print("-"*50 + "\n")

def testThread(a, b):
    print(threading.current_thread().getName(), a)
    print(threading.current_thread().getName(), b)

def startThread():
    projectList = [
        "Time"
    ]
    versionList0 = []
    versionList1 = []
    versionList2 = []
    # versionList3 = []
    for i in range(22, 24):
        versionList0.append(str(i))
    for i in range(24, 26):
        versionList1.append(str(i))
    for i in range(26, 28):
        if str(i) == 21:
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
if __name__ == '__main__':
    # startThread()
    getMutant(["Time"], ["1"])

       
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
