# SSH 生成git公钥 

## windows平台
1. 安装SSH，安装git的windows版本会自动安装
2. 使用`ssh-keygen`命令生成公钥
```
$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/c/Users/Administrator/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /c/Users/Administrator/.ssh/id_rsa.
Your public key has been saved in /c/Users/Administrator/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:WilFx+8GD3u2N1zR1gqt8z2v8ydbXtBPRy8Uh2tdm4Y Administrator@USER-20190920CN
The key's randomart image is:
+---[RSA 3072]----+
|        ...   ...|
|       . ..   .o.|
|        .  . .ooB|
|       . .o oE+B*|
|      . S  * ++o*|
|       +  . O .++|
|      .    + = o+|
|            . B++|
|             .oBB|
+----[SHA256]-----+
```
3. 将生成的公钥文件打开，公钥文件的位置`/c/Users/Administrator/.ssh/id_rsa.pub`，复制公钥，然后在github的个人设置中添加公钥即可
## linux平台
linux平台也是类似的操作，不在重复