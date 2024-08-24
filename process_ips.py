import requests
import gzip
import shutil
import os

# 配置下载 ID 和文件名
file_id = '1gjn8Tgx0_xpFccIMO7sdCnAnaPWDAu9F'
url_template = 'https://drive.usercontent.google.com/uc?id={file_id}&export=download'
compressed_filename = 'file.gz'
decompressed_filename = 'ipv4'
dns_txt_filename = 'dns.txt'
dns_yaml_filename = 'DNS.yaml'

# 生成下载 URL
url = url_template.format(file_id=file_id)

# 下载文件
def download_file(url, local_filename):
    print(f"Downloading {url} to {local_filename}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

# 解压缩文件
def decompress_gz_file(gz_filename, output_filename):
    print(f"Decompressing {gz_filename} to {output_filename}")
    with gzip.open(gz_filename, 'rb') as f_in:
        with open(output_filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

# 处理文件并生成输出
def process_file(input_filename):
    print(f"Processing {input_filename}")
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    dns_txt_lines = []
    dns_yaml_lines = ["payload:"]
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 2:
            continue  # 跳过无效行
        ip = parts[1]
        cidr_ip = f"{ip}/32"
        dns_txt_lines.append(f"IP-CIDR,{cidr_ip}")
        dns_yaml_lines.append(f"  - '{cidr_ip}'")

    with open(dns_txt_filename, 'w') as file:
        file.write('\n'.join(dns_txt_lines) + '\n')

    with open(dns_yaml_filename, 'w') as file:
        file.write('\n'.join(dns_yaml_lines))

# 运行步骤
if __name__ == "__main__":
    # 下载压缩文件
    download_file(url, compressed_filename)

    # 解压缩文件
    decompress_gz_file(compressed_filename, decompressed_filename)

    # 处理解压后的文件
    process_file(decompressed_filename)

    # 清理临时文件
    os.remove(compressed_filename)
    os.remove(decompressed_filename)
