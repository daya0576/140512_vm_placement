import common_funs.comm_funs as comm
import xlwt

def list2xls(input_name, output_name):   
    fileList = comm.read_list_from_file(input_name)
    print fileList
    
    wfile = xlwt.Workbook()
    table = wfile.add_sheet("1")
    
    for k, num in enumerate(fileList):
        table.write(0, k, str(num))
        if k > 50:
            break
    wfile.save(output_name)

input = "test/exp/final_cpu_result"
output = "test/exp/final_cpu_result.xls"   
list2xls(input, output)  