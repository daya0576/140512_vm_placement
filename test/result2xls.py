import re
import xlwt
import os
import time
local_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))

fileList = ['1Partitions@15percent', '1Partitions@5percent',
             '2Partitions@15percent', '2Partitions@5percent',
             '3Partitions@15percent', '3Partitions@5percent',
             '4Partitions@15percent', '4Partitions@5percent',
             '5Partitions@15percent', '5Partitions@5percent']
methods = [" -a ", " -m ", " -n ", " -h ", " -b ", " -ncut ", "-ncc", " -rcut ", " -rcc "]
pmTypes = ["Node1024_cpu0.5_men0.3_stdvar1", 
           "Node1024_cpu0.5_men0.5_stdvar1", 
           "Node1024_cpu0.2_men0.2_stdvar1"]

def read_line_from_file(os_path):
    with open(os_path) as f:
        line_result = f.readlines()
    
    return line_result

def findAllResult(souceFile):
    xls_lists = []
    xls_list = []
    b = re.compile(r"\d+\.\d*")  
    lines = read_line_from_file(souceFile)
    for line in lines:
        if "sum(distace * flow)" in line:
            xls_list.append(float(b.findall(line)[0]))
        elif ("Node1024" in line or "Done" in line):
            if len(xls_list) != 0:
                xls_lists.append(xls_list)
            xls_list = []
            
    return xls_lists    

def handleXLSFile(fileList):
    wfile = xlwt.Workbook()
    table = wfile.add_sheet("1")
    
    for k, souceFile in enumerate(fileList):
        os_path = local_date + "/" + souceFile + "_test.txt"
        if os.path.exists(os_path):
            xls_lists = findAllResult(os_path)
            table.write(0+k*4, 0, souceFile)
            for i in range(len(pmTypes)):
                #print pmTypes[i][9:22]
                table.write(i+1+k*4, 0, pmTypes[i][9:22])
            for j in range(len(methods)):
                table.write(0+k*4, j+1, methods[j])
            for i, line in enumerate(xls_lists):
                
                for j, result in enumerate(line):
                    table.write(i+1+k*4, j+1, result)
            
    wfile.save(local_date + "/test_all_" + local_date + ".xls")
            
            
if __name__ == "__main__" :
    handleXLSFile(fileList)
            


    
    
    
    
    
    
    
    
    