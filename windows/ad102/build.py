"""Compile x64 EFI; never install, sign or execute it."""
import argparse,hashlib,json,struct,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--clang',default='clang');p.add_argument('--linker',default='lld-link');p.add_argument('--enable-experiment',action='store_true');a=p.parse_args()
root=Path(__file__).resolve().parent/'source'
if a.enable_experiment and '0,0,0,{0,0,0,0,0,0,0,0}' in (root/'unlock/local_profile.h').read_text():p.error('Set reviewed local Windows ESP GUID in source/unlock/local_profile.h first')
out=root/'build';out.mkdir(exist_ok=True)
names=['app','app_io','ownership','format','runtime','sha256','checks','port','compat','vendor/unlock_610','vendor/prep_610','vendor/layout_610','vendor/vbios_610','vendor/gfw_eval']
flags=['--target=x86_64-pc-windows-msvc','-c','-std=c11','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-red-zone','-fshort-wchar','-Os','-Wall','-Wextra','-Werror','-Wno-unused-parameter','-D__KERNEL__','-DGU_UEFI_PORT','-DGU_TARGET_PCI_ID=0x268410deU','-Iunlock','-Iunlock/compat','-Ideps/edk2/MdePkg/Include','-Ideps/edk2/MdePkg/Include/X64']
if a.enable_experiment:flags+=['-DKOH_ENABLE_EXPERIMENT=1']
objects=[]
for name in names:
 obj=out/(name.replace('/','_')+'.obj');subprocess.run([a.clang,*flags,'unlock/'+name+'.c','-o',str(obj)],cwd=root,check=True);objects.append(str(obj))
efi=out/'BOOTX64.EFI'
subprocess.run([a.linker,'/subsystem:efi_application','/entry:EfiMain','/nodefaultlib','/machine:x64','/dynamicbase','/nxcompat','/fixed:no','/timestamp:0','/out:'+str(efi),*objects],check=True)
b=efi.read_bytes();pe=struct.unpack_from('<I',b,60)[0];opt=pe+24
assert b[:2]==b'MZ' and b[pe:pe+4]==b'PE\0\0'
assert struct.unpack_from('<H',b,pe+4)[0]==0x8664 and struct.unpack_from('<H',b,opt+68)[0]==10
assert struct.unpack_from('<I',b,opt+156)[0]>0
for i in (1,9,12,13,14):assert b[opt+112+i*8:opt+120+i*8]==bytes(8)
print(json.dumps({'sha256':hashlib.sha256(b).hexdigest(),'size':len(b),'execution_enabled':a.enable_experiment,'hardware_tested_public_build':False},indent=2))
