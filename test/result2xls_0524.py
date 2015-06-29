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

def findAllAverHop(souceFile):
    xls_lists = []
    xls_list_best = []
    xls_list_first = []
    b = re.compile(r"\d+\.\d*")
    lines = read_line_from_file(souceFile)
    for line in lines:
        if "Best fit:" in line:
            flag = 0
        elif "First fit: " in line:
            flag = 1
        elif "tabu search" in line:
            flag = -1
        if "2.Average Hops" in line:
            #xls_list.append(float(b.findall(line)[0]))
            if flag is 0:
                xls_list_best.append(float(line[27:32]))
            elif flag is 1:
                xls_list_first.append(float(line[27:32]))
            else:pass
            
                
        elif ("Node1024" in line or "Done" in line):
            if len(xls_list_best) != 0:
                xls_lists.append(xls_list_best)
                xls_lists.append(xls_list_first)
            xls_list_best = []
            xls_list_first = []
         
    return xls_lists    

def findAllTobu(souceFile):
    xls_lists = []
    xls_list_best = []
    xls_list_first = []
    b = re.compile(r"\d+\.\d*")
    lines = read_line_from_file(souceFile)
    for line in lines:
        if "Best fit:" in line:
            flag = 0
        elif "First fit: " in line:
            flag = 1
        if "tabu search:" in line:
            #xls_list.append(float(b.findall(line)[0]))
            if flag is 0:
                xls_list_best.append(float(b.findall(line)[0]))
            elif flag is 1:
                xls_list_first.append(float(b.findall(line)[0]))
            else:pass
            
                
        elif ("Node1024" in line or "Done" in line):
            if len(xls_list_best) != 0:
                xls_lists.append(xls_list_best)
                xls_lists.append(xls_list_first)
            xls_list_best = []
            xls_list_first = []
         
    return xls_lists    

def findAllSum(souceFile):
    xls_lists = []
    xls_list_best = []
    xls_list_best_tabu = []
    xls_list_first = []
    xls_list_first_tabu = []
    b = re.compile(r"\d+\.\d*")
    lines = read_line_from_file(souceFile)
    for line in lines:
        if "Best fit:" in line:
            flag = 1
        if "First fit: " in line:
            flag = 3
        if "tabu search: " in line:
            if flag == 1:
                flag = 2   
        if "tabu search: " in line:
            if flag == 3:
                flag = 4
        b = re.compile(r"\d+\.\d*")
        if "sum(distace * flow)" in line:
            #xls_list.append(float(b.findall(line)[0]))
            if flag is 1:
                xls_list_best.append(float(b.findall(line)[1]))
            elif flag is 3:
                xls_list_first.append(float(b.findall(line)[1]))
            elif flag is 2:
                xls_list_best_tabu.append(float(b.findall(line)[1]))
            elif flag is 4:
                xls_list_first_tabu.append(float(b.findall(line)[1]))
            
            else:pass
            
                
        elif ("Node1024" in line or "Done" in line):
            if len(xls_list_best) != 0:
                xls_lists.append(xls_list_best)
                xls_lists.append(xls_list_best_tabu)
                xls_lists.append(xls_list_first)
                xls_lists.append(xls_list_first_tabu)
            xls_list_best = []
            xls_list_first = []
         
    return xls_lists    

def findAllLayer(souceFile):
    xls_lists = []
    xls_list = []
    xls_list_core = []
    xls_list_aggr = []
    xls_list_edge = []
    b = re.compile(r"\d+\.\d*")  
    lines = read_line_from_file(souceFile)
    for line in lines:
        if "Best fit:" in line:
            flag_first = 0
            flag_tabu = 0
        elif "tabu search:" in line:
            flag_tabu = 1
        elif "First fit:" in line:
            flag_first =1
            flag_tabu = 0
        elif "method" in line:
            flag_tabu = 0
        
        if "3.Core:" in line:
            if flag_tabu == 0 and flag_first == 0:
                print b.findall(line)
                xls_list_core.append(float(b.findall(line)[1]))
                xls_list_aggr.append(float(b.findall(line)[2]))
                xls_list_edge.append(float(b.findall(line)[3]))
        #elif ("Node1024" in line or "Done" in line):
        
        elif ("Done" in line):
            print "Done"
            xls_lists.append(xls_list_core)
            xls_lists.append(xls_list_aggr)
            xls_lists.append(xls_list_edge)
            print "xls_lists", xls_lists
            xls_list_core = []
            xls_list_aggr = []
            xls_list_edge = []
            
    return xls_lists    

def findAllSumTree(souceFile):
    xls_lists = []
    xls_list = []
    
    b = re.compile(r"\d+\.\d*")  
    lines = read_line_from_file(souceFile)
    for line in lines:
        if "Best fit:" in line:
            flag_first = 0
            flag_tabu = 0
        elif "tabu search:" in line:
            flag_tabu = 1
        elif "First fit:" in line:
            flag_first =1
            flag_tabu = 0
        elif "method" in line:
            flag_tabu = 0
        
        if "sum(distace * flow)" in line:
            if flag_tabu == 0 and flag_first == 0:
                print b.findall(line)
                xls_list.append(float(b.findall(line)[1]))
        #elif ("Node1024" in line or "Done" in line):
        
        elif ("Done" in line):
            print "Done"
            xls_lists.append(xls_list)
            print "xls_lists", xls_lists
            xls_list = []
            
    return xls_lists    

def handleXLSFile(xls_lists):
    wfile = xlwt.Workbook()
    table = wfile.add_sheet("1")
    
    for k, souceFile in enumerate(["1Partitions@5percent"]):
            table.write(0+k*4, 0, souceFile)
            for i in range(len(pmTypes)):
                #print pmTypes[i][9:22]
                table.write(i+1+k*4, 0, pmTypes[i][9:22])
            for j in range(len(methods)):
                table.write(0+k*4, j+1, methods[j])
            for i, line in enumerate(xls_lists):
                for j, result in enumerate(line):
                    table.write(i+1+k*4, j+1, result)
            
    wfile.save("test_all_" + local_date + ".xls")
            
if __name__ == "__main__" :
    filename = "2015-05-26_core/3Partitions@15percent_test_2.txt"
    filename = "2015-05-26_tree/5Partitions@5percent_test_2.txt"
    
    AverHop = findAllSumTree(filename)
    #AverHop = findAllSumTree("2015-05-26_core/5Partitions@5percent_test_2.txt")
    
    print AverHop
    for data in AverHop:
        print data 
    
    handleXLSFile(AverHop)       


    
    
    
    
    
    
    
    
    