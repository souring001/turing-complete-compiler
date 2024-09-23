# Compiler for LEG Architecture
ゲームTuring Completeに登場するLEGアーキテクチャ用に作ったコンパイラです．

Python風の高級言語から，アセンブリに変換します．

PythonのASTを使ってスタックマシンに変換したのちに，LEGのアセンブリ命令へと変換します．
出力するアセンブリは冗長なので，最後に最適化を行いました．

### 言語仕様
- レジスタ変数名(r2, r3, r4, r5)
- プログラムカウンタ：r6
- I/O：r7
- メモリへのアクセスはr5レジスタのみ
  - RAM[r5] = r2
  - r2 = RAM[r5]
- if文(条件式: `!=`, `==`, `<`)
- while文(条件式: `!=`, `==`, `<`)
- 演算(`+`, `-`)


### 例
最後のステージ「WATER WORLD」のプログラムは以下のように記述できます．

```py
r5 = 1
r3 = 0
while(r5 < 17):
    RAM[r5] = r7
    r5 = r5 - 1
    if r3 < RAM[r5]:
        r3 = RAM[r5]
    r5 = r5 + 33
    RAM[r5] = r3
    r5 = r5 - 31

r3 = 0
while(0 < r5):
    # RAM[r5 + 64] = max(RAM[r5 + 1], RAM[r5 + 1 + 64])
    r5 = r5 + 1
    if r3 < RAM[r5]:
        r3 = RAM[r5]
    r5 = r5 + 63
    RAM[r5] = r3 # 右壁の高さ[i]

    # min(左壁の高さ[i], 右壁の高さ[i]) - 高さ[i]
    r5 = r5 - 32 # i + 32
    if r3 < RAM[r5]:
        r4 = r3
    else:
        r4 = RAM[r5]
    r5 = r5 - 32 # i
    if RAM[r5] < r4:
        r4 = r4 - RAM[r5]
        r2 = r2 + r4
    r5 = r5 - 1 # i--

# 合計水量を出力
r7 = r2
```

### コンパイル
`main.py` 内にプログラムを記述して以下を実行します．

```sh
python main.py | python asm_converter.py | python asm_optimizer.py
```