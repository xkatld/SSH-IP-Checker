from flask import Flask, render_template, request, jsonify
import paramiko
import logging

app = Flask(__name__)

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

def get_ip_addresses(hostname, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)
        
        # 获取所有 IP 地址
        stdin, stdout, stderr = client.exec_command("ip addr show | grep inet")
        ip_output = stdout.read().decode().strip()
        
        # 解析 IP 地址
        internal_ipv4 = "N/A"
        internal_ipv6 = "N/A"
        public_ipv4 = "N/A"
        public_ipv6 = "N/A"
        
        for line in ip_output.split('\n'):
            if 'inet ' in line:
                internal_ipv4 = line.split()[1].split('/')[0]
            elif 'inet6' in line and not line.split()[1].startswith('fe80'):
                internal_ipv6 = line.split()[1].split('/')[0]
        
        # 尝试获取公网 IP
        stdin, stdout, stderr = client.exec_command("curl -s https://api.ipify.org")
        public_ipv4 = stdout.read().decode().strip()
        
        stdin, stdout, stderr = client.exec_command("curl -s https://api6.ipify.org")
        public_ipv6 = stdout.read().decode().strip()
        
        client.close()
        
        logging.debug(f"Internal IPv4: {internal_ipv4}")
        logging.debug(f"Internal IPv6: {internal_ipv6}")
        logging.debug(f"Public IPv4: {public_ipv4}")
        logging.debug(f"Public IPv6: {public_ipv6}")
        
        return internal_ipv4, internal_ipv6, public_ipv4, public_ipv6
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return str(e), str(e), str(e), str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hostname = request.form['hostname']
        port = int(request.form['port'])
        username = request.form['username']
        password = request.form['password']
        
        internal_ipv4, internal_ipv6, public_ipv4, public_ipv6 = get_ip_addresses(hostname, port, username, password)
        
        response = {
            'internal_ipv4': internal_ipv4,
            'internal_ipv6': internal_ipv6,
            'public_ipv4': public_ipv4,
            'public_ipv6': public_ipv6
        }
        logging.debug(f"Response: {response}")
        return jsonify(response)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
