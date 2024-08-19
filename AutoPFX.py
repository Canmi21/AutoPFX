import os
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import hashlib
import webbrowser
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True  # 保留引号

# 加载配置文件
def load_config():
    with open("Config.yaml", "r") as file:
        config = yaml.load(file)
    return config

# 加载密码文件
def load_passwords():
    if os.path.exists("Password.yaml"):
        with open("Password.yaml", "r") as file:
            passwords = yaml.load(file)
            if passwords is None:
                passwords = {}
    else:
        passwords = {}
    return passwords

# 保存密码
def save_password(pfx_file, password):
    passwords = load_passwords()

    if os.path.exists("Password.yaml"):
        with open("Password.yaml", "r") as file:
            yaml_data = yaml.load(file)
            if yaml_data is None:
                yaml_data = {}
    else:
        yaml_data = {}

    yaml_data.update(passwords)  # 更新而不是覆盖
    yaml_data[pfx_file] = password  # 添加新的密码项

    with open("Password.yaml", "w") as file:
        yaml.dump(yaml_data, file)

# 删除指定 PFX 文件的密码
def delete_password(pfx_file):
    passwords = load_passwords()

    if pfx_file in passwords:
        del passwords[pfx_file]

        with open("Password.yaml", "w") as file:
            yaml.dump(passwords, file)

# 读取 SignTool_Config.yaml 文件
def load_ps_script_template():
    with open(os.path.join("PFX", "SignTool_Config.yaml"), "r") as file:
        config = yaml.load(file)
    return config.get("PowerShellScript", "")

# 替换 PowerShell 脚本中的变量
def replace_ps_script_variables(template, pfx_name, pfx_subject, pfx_password):
    return template.format(pfx_name=pfx_name, pfx_subject=pfx_subject, pfx_password=pfx_password)

# 创建并执行 PowerShell 脚本
def create_and_run_ps_script(ps_script):
    ps_script_path = os.path.join("PFX", "Build.ps1")
    with open(ps_script_path, "w") as file:
        file.write(ps_script)
    
    # 执行 PowerShell 脚本
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_script_path], check=True)

# 显示主菜单
def show_main_menu(window):
    for widget in window.winfo_children():
        widget.destroy()

    label = tk.Label(window, text="Please select an option:", font=("Arial", 14))
    label.pack(pady=20)

    inject_button = tk.Button(window, text="Inject PFX", command=lambda: inject_pfx(window), width=15)
    inject_button.pack(pady=10)

    create_button = tk.Button(window, text="Create PFX", command=lambda: create_pfx_menu(window), width=15)
    create_button.pack(pady=10)

    about_button = tk.Button(window, text="About", command=show_about, width=15)
    about_button.pack(pady=10)

# 注入 PFX 文件
def inject_pfx(window):
    config = load_config()
    pfx_folder = config.get("PFX", "PFX")
    files = [f for f in os.listdir(pfx_folder) if f.endswith(".pfx")]

    for widget in window.winfo_children():
        widget.destroy()

    label = tk.Label(window, text="Select a PFX file to inject:", font=("Arial", 14))
    label.pack(pady=20)

    if not files:
        messagebox.showinfo("Info", f"No PFX files found in the folder: {pfx_folder}")
        show_main_menu(window)
    else:
        for file in files:
            button = tk.Button(window, text=file, command=lambda f=file: select_pfx(window, f))
            button.pack(pady=5)

    back_button = tk.Button(window, text="Back", command=lambda: show_main_menu(window), width=15)
    back_button.pack(pady=20)

# 选择 PFX 文件
def select_pfx(window, file):
    passwords = load_passwords()
    if file in passwords:
        list_exe_files(window, file)
    else:
        password = simpledialog.askstring("Input", f"Enter password for {file}:", show='*')
        if password:
            save_password(file, password)
            inject_pfx(window)

# 列出所有 EXE 文件
def list_exe_files(window, pfx_file):
    for widget in window.winfo_children():
        widget.destroy()

    exe_files = []
    start_dir = os.getcwd()
    for root, dirs, files in os.walk(start_dir):
        depth = root[len(start_dir):].count(os.sep)
        if depth < 10:  # 控制遍历深度
            for file in files:
                if file.lower().endswith(".exe"):  # 忽略大小写
                    exe_files.append(os.path.join(root, file))

    label = tk.Label(window, text="Found .exe files:", font=("Arial", 14))
    label.pack(pady=20)

    if not exe_files:
        no_files_label = tk.Label(window, text="No .exe files found.", font=("Arial", 12))
        no_files_label.pack(pady=10)
    else:
        for exe in exe_files:
            frame = tk.Frame(window, width=800)  # 调整宽度
            frame.pack(fill="x", padx=10, pady=2)

            # 计算 SHA256 哈希
            sha256_hash = hashlib.sha256()
            with open(exe, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            sha256_digest = sha256_hash.hexdigest()

            exe_label = tk.Label(frame, text=exe, font=("Arial", 10), anchor="w", justify="left")
            exe_label.pack(side="left", fill="x", expand=True)

            sha256_label = tk.Label(frame, text=sha256_digest, font=("Arial", 10), anchor="e", justify="right")
            sha256_label.pack(side="left", padx=5)

            add_button = tk.Button(frame, text="+", width=2, command=lambda e=exe: sign_exe(window, pfx_file, e))
            add_button.pack(side="left", padx=5)

            info_button = tk.Button(frame, text="i", width=2, command=lambda e=exe: show_signature_info(e))
            info_button.pack(side="right", padx=5)

    back_button = tk.Button(window, text="Back", command=lambda: inject_pfx(window), width=15)
    back_button.pack(pady=20)

# 显示 EXE 文件的签名信息
def show_signature_info(exe_file):
    config = load_config()
    sign_tool_path = config.get("SignToolPath")
    
    if not sign_tool_path or not os.path.exists(sign_tool_path):
        messagebox.showerror("Error", "SignToolPath not found in Config.yaml or invalid path. Please check the configuration.")
        return

    try:
        command = [sign_tool_path, "verify", "/pa", exe_file]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Signature Info", result.stdout)
        else:
            messagebox.showinfo("No Signature", "No valid signature found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# 签名 EXE 文件
def sign_exe(window, pfx_file, exe_file):
    config = load_config()
    sign_tool_path = config.get("SignToolPath")
    timestamp_url = config.get("TimeStampUrl")

    if not sign_tool_path or not timestamp_url:
        messagebox.showerror("Error", "SignToolPath or TimeStampUrl not found in Config.yaml. Please check the configuration.")
        return

    passwords = load_passwords()
    password = passwords.get(pfx_file)

    try:
        # 直接使用 PFX 文件和密码进行签名
        command = [
            sign_tool_path,
            "sign",
            "/f", os.path.join(config["PFX"], pfx_file),
            "/p", password,
            "/tr", timestamp_url,
            "/td", "sha256",
            "/fd", "sha256",
            exe_file
        ]
        subprocess.run(command, check=True)

        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 签名成功提示
        messagebox.showinfo("Signed Successfully", f"""
        {os.path.basename(exe_file)}
        {exe_file}
        {pfx_file}
        {current_time}
        """)

    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Signing failed. Please check the password and try again.")
        delete_password(pfx_file)
        select_pfx(window, pfx_file)

# 使用 PowerShell 创建 PFX 证书页面
def create_pfx_menu(window):
    config = load_config()
    pfx_folder = config.get("PFX")

    if not pfx_folder:
        messagebox.showerror("Error", "PFX storage path not found in Config.yaml. Please check the configuration.")
        return

    for widget in window.winfo_children():
        widget.destroy()

    label = tk.Label(window, text="Create a new PFX certificate:", font=("Arial", 14))
    label.pack(pady=20)

    tk.Label(window, text="PFX File Name:", font=("Arial", 12)).pack(pady=5)
    pfx_name_entry = tk.Entry(window, width=30)
    pfx_name_entry.pack(pady=5)

    tk.Label(window, text="PFX Display Name:", font=("Arial", 12)).pack(pady=5)
    pfx_display_name_entry = tk.Entry(window, width=30)
    pfx_display_name_entry.pack(pady=5)

    tk.Label(window, text="PFX Password:", font=("Arial", 12)).pack(pady=5)
    pfx_password_entry = tk.Entry(window, show='*', width=30)
    pfx_password_entry.pack(pady=5)

    def validate_and_create_pfx():
        pfx_name = pfx_name_entry.get().strip()
        pfx_display_name = pfx_display_name_entry.get().strip()
        pfx_password = pfx_password_entry.get().strip()

        if not pfx_name or not pfx_display_name or not pfx_password:
            messagebox.showerror("Error", "All fields are required.")
            return

        if any(char in pfx_name for char in r'\/:*?"<>|'):
            messagebox.showerror("Error", "PFX file name contains invalid characters.")
            return

        if not os.path.exists(pfx_folder):
            os.makedirs(pfx_folder)

        # 加载 PowerShell 脚本模板
        ps_script_template = load_ps_script_template()

        # 替换模板中的变量
        ps_script = replace_ps_script_variables(ps_script_template, pfx_name, pfx_display_name, pfx_password)

        try:
            # 生成并执行 PowerShell 脚本
            create_and_run_ps_script(ps_script)

            # 保存密码
            save_password(f"{pfx_name}.pfx", pfx_password)

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            timestamp_url = config.get("TimeStampUrl", "")

            # 创建成功提示
            messagebox.showinfo("PFX Created Successfully", f"""
            {pfx_name}.pfx
            {pfx_display_name}
            {timestamp_url}
            {current_time}
            """)

            show_main_menu(window)

        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to create the PFX file. Please check the configuration.")

    cancel_button = tk.Button(window, text="Cancel", command=lambda: show_main_menu(window), width=15)
    cancel_button.pack(side="left", padx=10, pady=20)

    create_button = tk.Button(window, text="Create", command=validate_and_create_pfx, width=15)
    create_button.pack(side="right", padx=10, pady=20)

# 关于
def show_about():
    webbrowser.open("https://github.com/Canmi21/AutoPFX")
    messagebox.showinfo("About AutoPFX", """
    AutoPFX GUI 2024 X Github.com
    OpenSource Software MIT license.
    Copyright (C) Canmi(Canmi21), all right reserved.
    """)

# 程序入口
def main():
    window = tk.Tk()
    window.title("AutoPFX Command Interface")
    window.geometry("800x600")

    show_main_menu(window)

    window.mainloop()

if __name__ == "__main__":
    main()
