# claude-spinner-verbs-japanese

Claude Code が作業中に表示する動詞（`Pondering…` `Schlepping…` など）を、**発音記号・日本語訳・語源の背景**を添えた日本語版に差し替える設定データ。

```
✻ Considering(kənˈsɪdərɪŋ)… 検討しています… （ラテン語 sidus＝星。星を観て吉凶を占う占星術に由来する語）…
✻ Reticulating(rɪˈtɪkjəleɪtɪŋ)… 網目にしています… （都市開発ゲーム SimCity 2000 の読み込み画面に出る
  Reticulating splines。開発者が意味のない言葉として入れた）…
✻ Thundering(ˈθʌndərɪŋ)… 鳴り響いています… （北欧神話の雷神 Thor と同語源。木曜 Thursday もこの神の名から）…
```

見慣れない語が出てきたときに、その場で意味と由来が分かる。`Flibbertigibbeting` や `Boondoggling` のように辞書を引かないと分からない語が組み込みには多く含まれている。

## 収録内容

Claude Code 本体に組み込まれている動詞をすべて収録している。並び順も本体と揃えてあるので差分が追いやすい。各行の形式は次のとおり。

```
語(発音記号)… 日本語訳… （語源の背景）
```

- **発音記号** — 国際音声記号（IPA）。米音基準。結合文字を含まない単一コードポイントのみを使用
- **日本語訳** — 一般的な訳語を進行形で。語源に引きずられた訳語は使わない（例: `Cooking` は「煮炊き」ではなく「料理」）
- **語源の背景** — 由来する言語と原義、そこから派生した語や逸話。固有名詞には「それが何か」を必ず添える。**定説がない語は「語源不明」「〜説がある」と明示**しており、断定していない（Puzzling, Shenaniganing, Canoodling, Flummoxing, Skedaddling, Moseying, Swirling, Julienning, Finagling, Lollygagging, Smooshing, Shimmying, Topsy-turvying, Tinkering）

## 使い方

`spinner-verbs.json` の内容を `~/.claude/settings.json` にマージする。

```bash
git clone git@github.com:crgstar/claude-spinner-verbs-japanese.git
cd claude-spinner-verbs-japanese
jq -s '.[0] * .[1]' ~/.claude/settings.json spinner-verbs.json > /tmp/s.json \
  && mv /tmp/s.json ~/.claude/settings.json
```

反映されるのは次に Claude Code を起動したときから。

`mode` の意味は次のとおり（Claude Code の公式設定）。

| mode | 挙動 |
|---|---|
| `replace` | このリポジトリの語だけを使う（本リポジトリの既定） |
| `append` | 組み込みの英語の語の後ろに足す |

`replace` で `verbs` が空配列だと組み込みの既定リストに戻る仕様なので、反映されないときはそこを確認する。

## 本体側の変更を検出する

Claude Code の更新で語が増減しても気付けないので、照合スクリプトを同梱している。

```console
$ ./check-upstream.py
差分なし
```

差分があると、増えた語と消えた語を並べて exit code 1 を返す。

```console
$ ./check-upstream.py
本家に増えた語:
  + Whittling

spinner-verbs.json を更新する
```

`~/.local/share/claude/versions/` にある最新のバイナリから動詞の配列を直接読み出して比較する。バイナリが見つからない、あるいは本体の構造が変わって配列を取り出せない場合は exit code 2 で止まる（差分なしと誤報しない）。

なお `Flambéing` と `Sautéing` は本体内で `é` が `\xE9` としてエスケープされているため、単純な文字列走査では取りこぼす。スクリプトはこれをデコードして扱う。

## 表示幅について

1 行が長い。日本語訳と背景を入れているので、経過時間や `esc to interrupt` の表示と合わせると、ターミナルの横幅が足りないときは折り返して 2 行になる。

短くしたい場合は、発音記号・日本語訳・背景の後半（派生や逸話の部分）のいずれかを削ると詰められる。

## 補足

動詞は 1 ターンにつき 1 語がランダムに選ばれる。ただしタスクリストの実行中表示やツールの件名がある間はそちらが優先されるため、動詞が見えるのは主に考えている最中。
