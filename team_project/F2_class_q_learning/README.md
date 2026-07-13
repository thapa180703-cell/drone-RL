# F2 Class Q-Learning (Starter)

## 課題概要
この課題は、class を使って Q-learning を実装する starter です。

F2の目的は、
高度な強化学習AIを完成させることではありません。

目的は、
- Environment class
- Agent class

を分けて、
- 状態（state）
- 行動（action）
- 報酬（reward）
- 学習（learning）

の流れを整理して理解することです。

## 学習目標
- state / action / reward を説明できる
- Q-table の役割を説明できる
- exploration と exploitation の違いを説明できる
- learning curve を見て学習の進み方を観察できる
- classベースで RL コードを整理できる

## F2は class版 Q-learning
F2では、役割を分けて実装します。

- `GridWorld`（Environment class）: 環境ルールを担当
- `QLearningAgent`（Agent class）: 行動選択と学習を担当

この分離により、実際のAI/RL開発に近い構造になります。

## Environment classとは何か
Environment class は、
「世界のルール」を持つクラスです。

例:
- 初期位置に戻す（reset）
- 行動を受け取って次状態を返す（step）
- 報酬と終了判定を返す

## Agent classとは何か
Agent class は、
「学習して行動を決める主体」を表すクラスです。

例:
- ε-greedyで行動を選ぶ
- Q-tableを更新する
- 複数episodeで学習する

## GridWorldの説明
GridWorld は、強化学習入門でよく使われるシンプルな環境です。

- マス目世界
- スタート地点
- ゴール地点
- エージェント

シンプルなので、学習アルゴリズムそのものに集中できます。

## state / action / reward の説明
- state: 現在の位置（例: `(1, 2)`）
- action: 選べる行動（up/down/left/right）
- reward: 行動結果の評価（ゴール到達で大きめ、通常移動は小さな負値）

## Q-table の説明
Q-table は、
「その状態で、各行動がどれくらい良さそうか」を保存する表です。

F2では以下の形を使います。

```python
q_table.shape == (grid_x, grid_y, action_count)
```

## exploration / exploitation の説明
- exploration（探索）: 新しい行動を試す
- exploitation（活用）: 今までの学習結果で最善行動を選ぶ

ε-greedy は、この2つをバランスするための基本手法です。

## learning curve の説明
learning curve は、
episodeごとの total reward を描いたグラフです。

- x軸: episode
- y軸: total reward

学習が進んでいるかを確認するために使います。

## Q-table visualization の説明
各状態の最大Q値をヒートマップ表示します。

```python
np.max(q_table, axis=2)
```

色の濃淡で「どの場所が有利になってきたか」を確認できます。

## E2 Maze class との接続
E2では `Maze` class で迷路状態と探索処理をまとめました。

F2では、
- `GridWorld`（Environment）
- `QLearningAgent`（Agent）

に分けます。

```text
E2: Maze class
↓
F2: Environment class + Agent class
```

どちらも「状態管理を整理する」考え方が共通です。

## F1関数版との違い
- F1: 関数のみで実装し、Q-learningの流れをシンプルに理解する
- F2: classで責務を分離し、実開発に近い構造を学ぶ

## ファイル構成
- `README.md`: 課題説明
- `grid_world.py`: Environment class
- `q_agent.py`: Agent class と学習ロジック
- `main.py`: 実行エントリポイント
- `starter_explanation.ipynb`: 補助教材Notebook
- `requirements.txt`: 依存ライブラリ

## 実行方法
```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

実行すると以下を確認できます。
- 学習完了メッセージ
- greedy policy によるテスト経路
- learning curve
- Q-table heatmap

## TODO
- [ ] episodes を変更する
- [ ] alpha を変更する
- [ ] gamma を変更する
- [ ] epsilon を変更する
- [ ] grid_size を変更する
- [ ] reward を変更する
- [ ] goal position を変更する
- [ ] learning curve を観察する
- [ ] Q-table heatmap を観察する

## challenge
- 壁を追加する
- obstacle を追加する
- 報酬設計を変更する
- epsilon decay を実装する
- 最短経路に近づくか確認する
- policy arrow map を作る
- F1関数版とF2クラス版を比較する
- D3倒立振子制御との関係を調べる
- Deep Q Networkとの関係を調べる

## GitHub提出時の注意
- TODOを最低3項目以上進める
- challengeを最低1項目以上試す
- 変更したパラメータ（episodes/alpha/gamma/epsilon）をREADMEに記録する
- 学習結果の考察を自分の言葉でまとめる
