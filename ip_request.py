# 对'ip.txt'文件中的IP地址在IPIPNet网站上查询运营商及as号
import requests
import xlwt
import xlrd
import sys



input_file = 'ip.txt'   # input_file = sys.argv[1]

token_value = '3bac81345fd945a35030149f4263c09baa7dbf51'
out_file = 'IpResult.xls'
api_addr = 'https://ipapi.ipip.net/v2/query'


# 读取ip输入文件
def read_ip(the_input_file):
    file_type = the_input_file.split('.')[1]
    if file_type == 'xlsx' or file_type == 'xls':
        workbook = xlrd.open_workbook(the_input_file)
        sheet1 = workbook.sheets()[0]
        the_ips = sheet1.col_values(0)
    elif file_type == 'txt':
        f = open(the_input_file, "r")
        ipss = f.readlines()
        the_ips = map(lambda x: x.replace('\n', ''), ipss)
    else:
        print('File type not supported!')
        sys.exit()
    return the_ips


# 查询一个ip
def request_ip(the_token_value, the_api_addr, the_ip):
    line = asn = ''
    url = the_api_addr+'/'+the_ip+'?'+'token='+the_token_value
    response = requests.get(url)
    dic = response.json()

    print(dic)
    # dic['data']['info']
    

    if 'data' in dic.keys():
        dic_data = dic['data']
        if 'info' in dic_data.keys():
            dic_info = dic_data['info']
            if 'line' in dic_info.keys():
                line = dic_info['line']
            if 'asn_info' in dic_info.keys():
                asn = dic_info['asn_info'][0]['asn']
    return [line, asn]


# 查询所有ip，并写入结果文件
def request_ips(the_token_value, the_api_addr, the_ips, the_out_file):
    work_book = xlwt.Workbook()
    work_sheet = work_book.add_sheet('sheet1')
    work_sheet.write(0, 0, 'ip')
    work_sheet.write(0, 1, 'line')
    work_sheet.write(0, 2, 'asn')
    row = 1
    for ip in the_ips:
        result = request_ip(the_token_value, the_api_addr, ip)
        work_sheet.write(row, 0, ip)
        work_sheet.write(row, 1, result[0])
        work_sheet.write(row, 2, result[1])
        row += 1
    work_book.save(the_out_file)
    print('Request finished!')


if __name__ == "__main__":
    ips = read_ip(input_file)
    request_ips(token_value, api_addr, ips, out_file)
