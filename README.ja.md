# SellerSprite 市場調査と BI

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

ユーザーが明示した言語で出力し、指定がなければ依頼文の言語に従います。コマンド、スキル ID、JSON キー、列挙値、単位、引用原文は保持します。翻訳と原文を分け、言語から国・通貨・法域を推定しません。詳細仕様の該当資料を読み、既存の検証と権限確認を適用します。

## 導入と利用

リポジトリを取得し、下記のスキルディレクトリを既存の references、scripts、assets などと一緒にホストのスキル用ディレクトリへコピーします。名前と SKILL.md は変更しません。説明言語を変えるだけなら再導入は不要です。導入用コマンドの掲載は、導入済みや有効化済みを意味しません。

```sh
git clone https://github.com/PDBen-Auto/sellersprite-amazon-market-research-bi-skill.git
```

## SellerSprite 市場調査と BI

`sellersprite-bi-market-research`

検索意図から関連 ASIN を広げ、市場層を分け、エクスポートを親 ASIN 単位で重複排除して監査可能な BI を作ります。

スキルディレクトリ: `.`

**実装の根拠と依存関係**

明確な市場/用途、標準・詳細 XLSX と必要なキーワード表。Python 3 と openpyxl。オンラインは許可済み SellerSprite/ブラウザ。推定は Amazon 精算データではありません。

**入力**

範囲/日付/市場/採否規則。探索時 seed_keyword/seed_asins。条件付きのキーワード・標準・詳細表。任意の関連性/属性/成果先。認証情報は禁止。

**出力**

理由・詳細対象範囲付き候補 manifest、親/月/年/YTD/同期間/ブランド売上/順位変動、単一 dashboard.html、監査と欠損記録。

[実行手順 · 制約と停止条件 · 依頼例](references/i18n/ja.md)

> 次のスキルを使用してください： `$sellersprite-bi-market-research` — キーワードと競合表から直接市場 BI を作り、詳細未対象候補を売上分母に加えません。日本語で回答し、根拠、不明点、操作権限を維持してください。

## 言語対応と検証

本書は目的、前提、入出力、手順、例、制約をまとめた日本語運用ガイドです。全参考資料の逐語訳ではありません。詳細技術資料、過去事例、スクリプトのエラー、サンプル画面、画像は原言語のままです。必要に応じて日本語で説明できます。構造・リンク・重要制約を確認していますが、各言語の母語話者による校閲は未実施です。

納品前に入力、根拠、欠損、出力ファイルと元の完了条件を照合します。未実行の工程は未検証とし、終了コードの成功を業務上の検証成功と混同しません。
