# 学習記録アプリ（Study Log App）

複数科目を並行して学習する大学生が、自分の学習時間の配分を可視化するためのシンプルなWebアプリです。
![アプリ画面](スクリーンショット 2026-08-05 104642.png)
## 概要

- 科目・学習内容・学習時間（分）を記録できます（**入力**）
- 記録はSQLiteデータベースに保存され、科目ごとの合計学習時間が自動集計されます（**処理**）
- 学習履歴一覧と科目別集計表がブラウザに表示されます（**出力**）

## 使用技術

- バックエンド：Python / Flask
- データベース：SQLite（Dockerボリュームで永続化）
- フロントエンド：Flaskテンプレート（Jinja2）+ 素のCSS

## 実行方法（Docker）

前提：Docker / Docker Compose がインストールされていること

```bash
git clone <このリポジトリのURL>
cd study-log-app
docker compose up --build
```

起動後、ブラウザで以下にアクセスしてください。

```
http://localhost:5000
```

停止する場合は `Ctrl+C`、コンテナを削除する場合は `docker compose down` を実行してください。
データは Docker ボリューム（`study-log-data`）に保存されるため、コンテナを再作成してもデータは保持されます。

## 使い方

1. トップページの「学習を記録する」フォームに、科目・学習内容・学習時間（分）を入力して「記録する」を押す
2. 「科目別 合計学習時間」に集計結果が反映される
3. 「学習履歴」に記録が一覧表示される（不要な記録は「削除」で消去可能）

## ディレクトリ構成

```
study-log-app/
├── app.py              # Flaskアプリ本体
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── data/                # SQLiteデータベース（実行時に自動生成、Gitには含めない）
```

## 開発について

生成AI（Claude）を用いて、アプリ構成の提案、Flaskアプリ本体・HTMLテンプレート・Dockerfile・docker-compose.ymlの生成を行いました。
