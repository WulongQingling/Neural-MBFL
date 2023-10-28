import json
import logging
import os
import pickle
import sys
import paramiko
from execute.FOM import executeFom, generateFom
from execute.SOM import executeSom, generateSom
from tool.cal_tools import calFomMbfl, countFunctionSus
from tool.config_variables import (SOMfaultlocalizationResultPath, djSrcPath,
                                   faliingTestOutputPath,
                                   faultlocalizationResultPath, mbflMethods,
                                   mutantsFilePath, outputCleanPath, password,
                                   project, sbflMethod, sourcePath,
                                   tempSrcPath, tpydataPath)
from tool.logger_config import logger_config
from tool.other import checkAndCreateDir, clearDir, run
from tool.remote_transmission import (cp_from_remote, get_host_ip, ip,
                                      sftp_upload)
from datetime import datetime


def getSbflSus(project, version):
    """
    获取sbfl的怀疑度值
    :param project: 项目名
    :param version: 版本号
    :return: 错误行信息和怀疑度列表
    suspiciousSbfl存储格式:
    错误文件路径: {
        sbfl方法名:{
            行号: 怀疑度
            ...
            行号: 怀疑度
        }
    }
    faultLocalization存储格式:
    错误文件路径: [行号, ..., 行号]
    }
    """
    try:
        suspiciousSbflPath = os.path.join(
            faultlocalizationResultPath, project, version, "suspiciousSbfl.json")
        faultLocalizationPath = os.path.join(
            faultlocalizationResultPath, project, version, "faultLocalization.json")
        if not os.path.exists(suspiciousSbflPath) or not os.path.exists(faultLocalizationPath):
            print('\033[1;32m************** getSbflSus **************\033[0m')
            hugeToFilePath = os.path.join(
                outputCleanPath, project, version, "HugeToFile.txt")
            with open(hugeToFilePath, 'r') as f:
                hugeToFileList = f.readlines()
            hugeToFileList = [s.split('\t')[0] for s in hugeToFileList]
            delIndexPath = os.path.join(
                tpydataPath, project, version, "data_saveAgain_del_statement_index")
            with open(delIndexPath, 'rb') as f:
                delIndexList = pickle.load(f)
            faultPlusHugePath = os.path.join(
                outputCleanPath, project, version, "faultPlusHuge.in")
            with open(faultPlusHugePath, 'rb') as f:
                faultLineDic = pickle.load(f)
            susScorePath = os.path.join(
                tpydataPath, project, version, "sus_score")
            with open(susScorePath, 'rb') as f:
                susScoreList = pickle.load(f)
            faultFilesLine = dict()
            for fault in faultLineDic.keys():
                fileLineNum = list()
                for index in range(0, len(hugeToFileList)):
                    if hugeToFileList[index] in fault:
                        fileLineNum.append(index)
                faultFilesLine[fault] = fileLineNum
            faultSbflSus = dict()
            for num in faultFilesLine.keys():
                # print(num)
                sbflSus = dict()
                for item in sbflMethod:
                    sbflSus[item] = dict()
                    faultSbflSus[num] = dict()
                t = 0
                distance = 0
                tFlag = True
                tFlag2 = True
                for index in range(0, len(hugeToFileList)):
                    if index in faultFilesLine[num] and tFlag:
                        distance = index
                        tFlag = False
                        for i in range(0, len(faultLineDic[num])):
                            faultLineDic[num][i] = faultLineDic[num][i] - distance

                    if delIndexList[index] is False:
                        if index in faultFilesLine[num]:
                            for item in sbflMethod:
                                sbflSus[item][index-distance] = susScoreList[item][t]
                            tFlag2 = False
                        elif tFlag2 is False:
                            break
                        t += 1
                for method in list(sbflSus.keys()):
                    for key in list(sbflSus[method].keys()):
                        if sbflSus[method][key] == 0:
                            del sbflSus[method][key]
                    faultSbflSus[num][method] = dict(
                        sorted(sbflSus[method].items(), key=lambda x: x[1], reverse=True))
            checkAndCreateDir(os.path.join(faultlocalizationResultPath))
            checkAndCreateDir(os.path.join(
                faultlocalizationResultPath, project))
            checkAndCreateDir(os.path.join(
                faultlocalizationResultPath, project, version))
            with open(suspiciousSbflPath, 'w') as f:
                f.write(json.dumps(faultSbflSus, indent=2))
            with open(faultLocalizationPath, 'w') as f:
                f.write(json.dumps(faultLineDic, indent=2))
        with open(suspiciousSbflPath, 'r') as f:
            faultSbflSus = json.load(f)
        with open(faultLocalizationPath, 'r') as f:
            faultLineDic = json.load(f)
        if ip != '202.4.130.30':
            sftp_upload('202.4.130.30', 'fanluxi', password,
                     suspiciousSbflPath, suspiciousSbflPath)
        if ip != '202.4.130.30':
            sftp_upload('202.4.130.30', 'fanluxi', password,
                     faultLocalizationPath, faultLocalizationPath)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename
        print(f'\033[1;31mError in {file_name} at line {line_number}: {e}\033[0m')
        logging.error(f'Error in {file_name} at line {line_number}: {e}')
        return
    print('\033[1;32m************** getSbflSus SUCCESS **************\033[0m')
    return faultLineDic, faultSbflSus


# 一阶变异体
def FOM(project, version,configData):
    # print(project, version)
    logging.info(project + " " + version)
    try:
        faultLineDic, sbflSus = getSbflSus(project, version)
        print(faultLineDic)
        logging.info(faultLineDic)
        muInfoList = generateFom(project, version)
        resultList = executeFom(project, version, muInfoList,configData)
        calFomMbfl(project, version, muInfoList, resultList)
        # countFunctionSus(project, version)
        logging.info(project + " " + version + " success!")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename
        print(f'\033[1;31mError in {file_name} at line {line_number}: {e}\033[0m')
        logging.error(f'Error in {file_name} at line {line_number}: {e}')
        return


# 二阶变异体
def SOM(project, version):
    # print(project, version)
    logging.info(project + " " + version)
    try:
        faultLineDic, sbflSus = getSbflSus(project, version)
        # print(faultLineDic)
        logging.info(faultLineDic)
        muInfoList = generateSom(project, version)
        resultList = executeSom(project, version, muInfoList)
        # calFomMbfl(project, version, resultList)
        logging.info(project + " " + version + " success!")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename
        print(f'\033[1;31mError in {file_name} at line {line_number}: {e}\033[0m')
        logging.error(f'Error in {file_name} at line {line_number}: {e}')
        return

if __name__ == '__main__':
    clearDir(tempSrcPath)
    checkAndCreateDir(tempSrcPath)
    logger = logger_config(log_path='logs/output.log')
    logging.getLogger("paramiko").setLevel(logging.WARNING)
    # 10b XSQ
    with open("./failVersion.json", "r") as f:
        failVersion = json.load(f)
    with open('config.json', 'r') as configFile:
        configData = json.load(configFile)
    try:
        for projectDir in project.keys():
            # projectDir = "Cli"
            for versionNum in range(1, project[projectDir] + 1):
                versionDir = str(versionNum) + 'b'
                # versionDir = "5b"
                if not failVersion.get(projectDir) is None and versionDir in failVersion[projectDir]:
                    continue
                if ip != '202.4.130.30':
                    clearDir(djSrcPath)
                    clearDir(outputCleanPath)
                    clearDir(tpydataPath)
                    clearDir(faliingTestOutputPath)
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect("202.4.130.30", username="fanluxi",
                                password=password)
                    sftp = ssh.open_sftp()
                    try:
                        sftp.stat(os.path.join(
                            faultlocalizationResultPath, projectDir, versionDir))
                    except FileNotFoundError:
                        try:
                            sftp.stat(os.path.join(
                                faultlocalizationResultPath, projectDir))
                        except FileNotFoundError:
                            sftp.mkdir(os.path.join(
                                faultlocalizationResultPath, projectDir))
                        finally:
                            sftp.mkdir(os.path.join(
                                faultlocalizationResultPath, projectDir, versionDir))
                        if cp_from_remote(projectDir, versionDir):
                            FOM(projectDir, versionDir,configData)
                            # SOM(projectDir, versionDir)
                    finally:
                        sftp.close()
                        ssh.close()
                # elif not os.path.exists(os.path.join(faultlocalizationResultPath, projectDir, versionDir)):
                # try:
                #     os.makedirs(os.path.join(
                #         faultlocalizationResultPath, projectDir, versionDir))
                # finally:
                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                print(formatted_time)
                FOM(projectDir, versionDir,configData)
                        # SOM(projectDir, versionDir)
                # exit(1)
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename
        print(f'\033[1;31mError in {file_name} at line {line_number}: {e}\033[0m')
        logging.error(f'Error in {file_name} at line {line_number}: {e}')
