|パッケージ|説明|
|---|---|
|mypy|静的型チェッカー|
|flake8|PEP8に沿ったコードになってるかチェッカー|
|black|フォーマッター|
|pytest|テスト|
|isort|importをいい感じに並べ替えるやつ|
|python-jose|JWTトークンの生成と検証を行う|
|cryptography|一般的な暗号を扱えるようにする|
|PassLib|パスワードのハッシュ化に必要|

## 起動

```shell
uvicorn main:app --reload --host 0.0.0.0
```

## API Doc
- openapi.json
http://localhost:8000/openapi.json

- swagger-ui
http://localhost:8000/docs

- redoc
http://localhost:8000/redoc
