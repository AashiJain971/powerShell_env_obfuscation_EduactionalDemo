import os
import string
from pprint import pprint
import random

# Known environment variables (without username (hp in this device) because username obfuscated code is specific to a device and cant be used generally) to extract characters from
env_vars = [
    "ALLUSERSPROFILE", "CommonProgramFiles", "CommonProgramW6432",
    "ComSpec", "PATHEXT", "ProgramData", "ProgramFiles",
    "ProgramW6432", "PSModulePath", "PUBLIC", "SystemDrive", "SystemRoot", "windir"
]

# Building env_mapping dictionary
env_mapping = {}
for ch in string.printable:
    env_mapping[ch] = {}
    for var in env_vars:
        value = os.getenv(var)
        if value and ch in value:
            env_mapping[ch][var] = []
            for i, c in enumerate(value):
                if c == ch:
                    env_mapping[ch][var].append(i)

# pprint(env_mapping)
# print("\n")

# Obfuscating any string using env_mapping
def envhide_obfuscate(string):
    obfs_code=[]
    for ch in string:
        possible_vars=list(env_mapping[ch].keys())
        if not possible_vars:
            obfs_code.append(f"('{ch}')")
            continue
        chosen_var=random.choice(possible_vars)
        possible_indices=env_mapping[ch][chosen_var]
        chosen_index=random.choice(possible_indices)
        new_character=os.getenv(chosen_var)[chosen_index]
        # print(new_character," ",ch), ie new_char is ch only 
        pwsh_syntax=f"$env:{chosen_var}[{chosen_index}]"
        obfs_code.append(pwsh_syntax)
    return (obfs_code)

#Generating full obfuscated PowerShell expression
def pwshl_obfuscate(command):
    cmd_parts = envhide_obfuscate(command)

    # print(cmd_parts,"\n")

    cmd_expr = f"@({', '.join(cmd_parts)}) -join ''"
    return f"iex ({cmd_expr})"

#Real-life example
powerShell_command = 'Write-Output 420'
print(pwshl_obfuscate(powerShell_command))
