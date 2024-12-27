

这是一个Python脚本，用于将FASTQ格式的测序数据文件分割成3个部分。主要功能：

1. 文件输入处理：
```python
fn1=sys.argv[1]  # 获取输入文件名
# 根据文件是否为gzip压缩格式选择不同的打开方式
if 'gz' in fn1:
    dfh1=gzip.open(fn1,'r')
if 'gz' not in fn1:
    dfh1=open(fn1,'r')
```

2. 参数设置：
```python
size1=int(sys.argv[2])  # 第一片段大小
size2=int(sys.argv[3])  # 最后片段大小
trim1=5  # 上游需要修剪的碱基数
trim2=5  # 下游需要修剪的碱基数
```

3. 文件读取兼容性处理：
```python
# Python3和Python2的不同读取方式
if sys.version_info[0]==3:
    ID1=str(dfh1.readline().rstrip())[2:-1]
    line1=str(dfh1.readline().rstrip())[2:-1]
    plus1=str(dfh1.readline().rstrip())[2:-1]
    QS1=str(dfh1.readline().rstrip())[2:-1]
if sys.version_info[0]==2:
    ID1=dfh1.readline().rstrip()
    line1=dfh1.readline().rstrip()
    plus1=dfh1.readline().rstrip()
    QS1=dfh1.readline().rstrip()
```

4. 输出文件处理：
```python
rfhs=[]
for i in range(1,4):
    rfhs.append(open(fn1+'_r'+str(i)+'.fq','w'))
```

5. 主要处理逻辑：
```python
while line1:
    # 处理第一片段
    if len(line1[trim1:size1+trim1])>=30:
        rfhs[0].write(str(ID1)+'-1'+'\n'+str(line1[trim1:size1+trim1])+'\n'+str(plus1[0])+'\n'+str(QS1[trim1:size1+trim1])+'\n')
    # 处理中间片段
    if len(line1[trim1+size1:(-1*size2)-trim2])>=30:
        rfhs[0].write(str(ID1)+'-2'+'\n'+str(line1[trim1+size1:(-1*size2)-trim2])+'\n'+str(plus1[0])+'\n'+str(QS1[trim1+size1:(-1*size2)-trim2])+'\n')
    # 处理最后片段
    if len(line1[(-1*size2)-trim2:-1*trim2])>=30:
        rfhs[0].write(str(ID1)+'-3'+'\n'+str(line1[(-1*size2)-trim2:-1*trim2])+'\n'+str(plus1[0])+'\n'+str(QS1[(-1*size2)-trim2:-1*trim2])+'\n')
```

主要功能：
1. 接受FASTQ格式的输入文件（可以是普通文本或gzip压缩文件）
2. 将每条序列分成三个部分：
   - 开始部分（size1长度）
   - 中间部分
   - 结束部分（size2长度）
3. 对每个部分进行修剪（trim1和trim2）
4. 只输出长度大于等于30bp的片段
5. 输出为FASTQ格式，每个片段都保留质量分数

注意事项：
- 脚本同时支持Python2和Python3
- 输出的序列ID会加上-1、-2、-3后缀以区分不同片段
- 所有输出都写入到第一个输出文件中（rfhs[0]）



#!/usr/bin/python

#"usage: 3piece_read_split.py Input_file First_piece_size(bp) Last_piece_size(bp) upstream_to_trim(bp) downstream_to_trim(bp)"
import gzip
import sys
fn1=sys.argv[1]

if 'gz' in fn1:
        dfh1=gzip.open(fn1,'r')

if 'gz' not in fn1:
	dfh1=open(fn1,'r')
if sys.version_info[0]==3:
	ID1=str(dfh1.readline().rstrip())[2:-1]
	line1=str(dfh1.readline().rstrip())[2:-1]
	plus1=str(dfh1.readline().rstrip())[2:-1]
	QS1=str(dfh1.readline().rstrip())[2:-1]
if sys.version_info[0]==2:
	ID1=dfh1.readline().rstrip()
	line1=dfh1.readline().rstrip()
	plus1=dfh1.readline().rstrip()
	QS1=dfh1.readline().rstrip()
rfhs=[]

size1=int(sys.argv[2])
size2=int(sys.argv[3])
trim1=5
trim2=5

for i in range(1,4):
	rfhs.append(open(fn1+'_r'+str(i)+'.fq','w'))


while line1:
	if len(line1[trim1:size1+trim1])>=30:
		rfhs[0].write(str(ID1)+'-1'+'\n'+str(line1[trim1:size1+trim1])+'\n'+str(plus1[0])+'\n'+str(QS1[trim1:size1+trim1])+'\n')
	if len(line1[trim1+size1:(-1*size2)-trim2])>=30:
		rfhs[0].write(str(ID1)+'-2'+'\n'+str(line1[trim1+size1:(-1*size2)-trim2])+'\n'+str(plus1[0])+'\n'+str(QS1[trim1+size1:(-1*size2)-trim2])+'\n')
	if len(line1[(-1*size2)-trim2:-1*trim2])>=30:
		rfhs[0].write(str(ID1)+'-3'+'\n'+str(line1[(-1*size2)-trim2:-1*trim2])+'\n'+str(plus1[0])+'\n'+str(QS1[(-1*size2)-trim2:-1*trim2])+'\n')
	if sys.version_info[0]==3:
		ID1=str(dfh1.readline().rstrip())[2:-1]
		line1=str(dfh1.readline().rstrip())[2:-1]
		plus1=str(dfh1.readline().rstrip())[2:-1]
		QS1=str(dfh1.readline().rstrip())[2:-1]
	if sys.version_info[0]==2:
		ID1=dfh1.readline().rstrip()
		line1=dfh1.readline().rstrip()
		plus1=dfh1.readline().rstrip()
		QS1=dfh1.readline().rstrip()  

map(lambda x:x.close(),rfhs)
