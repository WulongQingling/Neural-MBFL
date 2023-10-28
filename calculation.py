import json
import logging
import os
import pickle
import sys

import paramiko
from execute.FOM import executeFom, generateFom
from execute.SOM import executeSom, generateSom
from tool.cal_tools import calSbfl, calFomMbfl, calTopNMbflAverage, calTopNMbflBest, calTopNMbflWorst, countFunctionSus
from tool.config_variables import (SOMfaultlocalizationResultPath, djSrcPath,
                                   faliingTestOutputPath,
                                   faultlocalizationResultPath, mbflMethods,
                                   mutantsFilePath, outputCleanPath, password,
                                   project, sbflMethod, sourcePath,
                                   tempSrcPath, tpydataPath)
from tool.count_data import countTonN
from tool.logger_config import logger_config
from tool.mbfl_formulas import (binary, crosstab, dstar, gp13, jaccard, naish1,
                                ochiai, op2, russell, turantula)
from tool.other import checkAndCreateDir, clearDir, run
from tool.remote_transmission import (cp_from_remote, get_host_ip, ip,
                                      sftp_upload)

if __name__ == '__main__':
    with open("./failVersion.json", "r") as f:
        failVersion = json.load(f)
    for projectDir in project.keys():
        projectDir = "Chart"
        for versionNum in range(1, project[projectDir] + 1):
            versionDir = str(versionNum) + 'b'
            # versionDir = "11b"
            if not failVersion.get(projectDir) is None and versionDir in failVersion[projectDir]:
                continue
            print(projectDir, versionDir)
            countFunctionSus(projectDir, versionDir)
            susResult, functionSus = calSbfl(projectDir, versionDir)
            
            susPath = os.path.join(
                faultlocalizationResultPath, projectDir, versionDir, "susStatement")
            for root, dirs, files in os.walk(susPath):
                for filename in files:
                    with open(susPath + "/" + filename, 'r') as f:
                        susResult = json.load(f)
                    topNResult = calTopNMbflAverage(
                        projectDir, versionDir, susResult, filename, "faultLocalization.json", "topNStatementAverage")
                    topNResult = calTopNMbflBest(
                        projectDir, versionDir, susResult, filename, "faultLocalization.json", "topNStatementBest")
                    topNResult = calTopNMbflWorst(
                        projectDir, versionDir, susResult, filename, "faultLocalization.json", "topNStatementWorst")
            
            susPath = os.path.join(
                faultlocalizationResultPath, projectDir, versionDir, "susFunction")
            for root, dirs, files in os.walk(susPath):
                for filename in files:
                    with open(susPath + "/" + filename, 'r') as f:
                        susResult = json.load(f)
                    topNResult = calTopNMbflAverage(
                        projectDir, versionDir, susResult, filename, "falutFunction.json", "topNFunctionAverage")
                    topNResult = calTopNMbflBest(
                        projectDir, versionDir, susResult, filename, "falutFunction.json", "topNFunctionBest")
                    topNResult = calTopNMbflWorst(
                        projectDir, versionDir, susResult, filename, "falutFunction.json", "topNFunctionWorst")
        countTonN(faultlocalizationResultPath, projectDir, "topNFunctionAverage")
        countTonN(faultlocalizationResultPath, projectDir, "topNFunctionBest")
        countTonN(faultlocalizationResultPath, projectDir, "topNFunctionWorst")
        exit(1)