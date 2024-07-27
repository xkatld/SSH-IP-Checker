from flask import Flask, render_template, request, jsonify
import paramiko

app = Flask(__name__)

def get_ip_addresses(hostname, port, username, password):
    try:
        # 创建SSH客户端
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 连接到服务器
        client.connect(hostname, port=port, username=username, password=password)
        
        # 执行命令获取内网IP
        stdin, stdout, stderr = client.exec_command("hostname -I | awk '{print $1}'")
        internal_ip = stdout.read().decode().strip()
        
        # 执行命令获取公网IP
        stdin, stdout, stderr = client.exec_command("curl -s ifconfig.me")
        public_ip = stdout.read().decode().strip()
        
        client.close()
        
        return internal_ip, public_ip
    except Exception as e:
        return str(e), str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hostname = request.form['hostname']
        port = int(request.form['port'])
        username = request.form['username']
        password = request.form['password']
        
        internal_ip, public_ip = get_ip_addresses(hostname, port, username, password)
        
        return jsonify({
            'internal_ip': internal_ip,
            'public_ip': public_ip
        })
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
