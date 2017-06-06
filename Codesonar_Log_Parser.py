# -*- coding: utf-8 -*-
"""
Copyright 2015 Joohyun Lee(ppiazi@gmail.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import sys
import os
import getopt
import xlsxwriter

__author__ = 'ppiazi'
__version__ = 'v0.0.1'

LOG_PTN_NEW = "New analysis"
LOG_PTN_FINISHED = "Finished analysis."

EXCEL_COLS = ["No", "Start_DATE", "Start_TIME", "Finished_TIME", "PROJECT", "Address"]

def parse_lines_new(i, lines):
    t_inx = lines[i-1].find("]")

    t_time_s = lines[i-1][t_inx + 2:].strip()

    t_inx = lines[i+1].find(":")
    t_project = lines[i+1][t_inx + 2:].strip()

    t_inx = lines[i+4].find(":")
    t_address = lines[i+4][t_inx + 2:].strip()

    return t_time_s, t_project, t_address

def parse_lines_finished(i, lines):
    t_inx = lines[i - 1].find("]")

    t_time_s = lines[i - 1][t_inx + 2:].strip()

    t_inx = lines[i + 1].find(":")
    t_project = lines[i + 1][t_inx + 2:].strip()

    return t_time_s, t_project

def analyze_codesonar_log(target_file):
    try:
        f = open(target_file, "r")
    except Exception as e:
        pass

    lines = f.readlines()

    log_list = []
    t = None
    i = 0
    for each_line in lines:
        if LOG_PTN_NEW in each_line:
            t_time, t_project, t_address = parse_lines_new(i, lines)

            t = {}
            t["s_time"] = t_time
            t["s_date"] = t_time[:10]
            t["e_time"] = ""
            t["project"] = t_project
            t["address"] = t_address

            print("%s / %s / %s" % (t["s_time"], t["project"], t["address"]))

            log_list.append(t)
        elif LOG_PTN_FINISHED in each_line:
            t_time, t_project = parse_lines_finished(i, lines)

            for item in log_list:
                if item["project"] == t_project and item["e_time"] == "":
                    item["e_time"] = t_time

        i = i + 1

    save_as_excel(target_file, log_list)

def save_as_excel(log_file, qac_log_list):
    excel_file_name = log_file + ".xlsx"

    wbk = xlsxwriter.Workbook(excel_file_name)
    sheet = wbk.add_worksheet("Codesonar_LOG")

    i = 0
    for col in EXCEL_COLS:
        sheet.write(0, i, col)
        i = i + 1

    i = 1
    for row in qac_log_list:
        sheet.write(i, 0, i)
        sheet.write(i, 1, row["s_date"])
        sheet.write(i, 2, row["s_time"])
        sheet.write(i, 3, row["e_time"])
        sheet.write(i, 4, row["project"])
        sheet.write(i, 5, row["address"])
        i = i + 1

    wbk.close()

def printUsage():
    print("Codesonar_Log_Parser.py [-f <file>]")
    print("    Version %s" % __version__)
    print("    Options:")
    print("    -f : set a target log file")

if __name__ == "__main__":
    optlist, args = getopt.getopt(sys.argv[1:], "f:")

    p_target_file = None

    for op, p in optlist:
        if op == "-f":
            p_target_file = p
        else:
            print("Invalid Argument : %s / %s" % (op, p))

    if p_target_file == None:
        printUsage()
        os._exit(1)

    analyze_codesonar_log(p_target_file)
