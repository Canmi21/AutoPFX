# AutoPFX
AutoPFX -- A GUI tool for automatically creating and deploying signatures.
## Usage
### Install Requitrment
``` shell
pip install ruamel.yaml
```
### Download Package
打开 [`Releases`](https://github.com/Canmi21/AutoPFX/releases/) 下载 `AutoPFX`

### Launch AutoPFX
打开 `AutoPFX.EXE`

## About
有关于本项目中所有打包的 `.EXE` 文件都使用了 `Canmi@Xyy` 类的签名，使用 `SHA256` 加密，虽然可以一定程度的避免被微软自带的防火墙清除掉，但是如果你的电脑还是自动清除了再核对下载文件的 `SHA256` 或者 `MD5` 值一致后请忽略风险警告，本项项目承诺所有文件开源免费，如果您好奇 `Package` 中的内容，请仔细查阅源码 

`AutoPFX.EXE` `14c14e81cf5dc658ea1df6eb221ab82b9b0f968fd530e612af4e311b3646672a`

您可以在 `PowerShell` 中使用 `certutil` 命令查询 `SHA256`
``` shell
certutil -hashfile AutoPFX.EXE  SHA256
```

从终端中得到的执行结果应该像这样:
``` shell
SHA256 hash of AutoPFX.EXE:
14c14e81cf5dc658ea1df6eb221ab82b9b0f968fd530e612af4e311b3646672a
CertUtil: -hashfile command completed successfully.
```
## View
![ ](/img/01.png)
![ ](/img/02.png)
![ ](/img/03.png)
![ ](/img/04.png)
![ ](/img/05.png)
![ ](/img/06.png)
![ ](/img/07.png)
![ ](/img/08.png)
![ ](/img/09.png)

## Acknowledgements
### * [XiangYang](https://github.com/XiangYyang)
### You
