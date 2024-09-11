#### Основные компоненты:

1. **Хеширование паролей с помощью bcrypt**
2. **Создание и верификация JWT токенов**
3. **API-методы для регистрации, входа и смены пароля**

---

### 1. **Хеширование паролей с помощью bcrypt**

**bcrypt** — это алгоритм хеширования, специально созданный для защиты паролей. Он включает в себя встроенную защиту от атак
типа "грубая сила" за счёт автоматического увеличения сложности хеширования (за счёт "соли" и настройки числа итераций).

- **Функция `hash_password`**:
    - Пароль перед хешированием кодируется в байтовую строку.
    - Используется функция `bcrypt.hashpw`, которая принимает сгенерированную "соль" (`bcrypt.gensalt()`) и пароль, и
      возвращает хешированное значение пароля.
    - Результат декодируется обратно в строку для удобного хранения в базе данных.

  Пример:
  ```python
  def hash_password(password: str) -> str:
      return bcrypt.hashpw(
          password.encode(),
          bcrypt.gensalt(),
      ).decode()
  ```

- **Функция `check_password`**:
    - Используется для проверки правильности пароля пользователя.
    - Пароль, введённый пользователем, кодируется в байтовую строку и сравнивается с хешем пароля, хранящимся в базе данных.
    - Функция возвращает `True`, если пароль верен, и `False` в противном случае.

  Пример:
  ```python
  def check_password(password: str, hashed_password: str) -> bool:
      return bcrypt.checkpw(
          password.encode(),
          hashed_password.encode(),
      )
  ```

**Особенности bcrypt**:

- **Соль** генерируется автоматически и добавляется к хешу. Это означает, что каждый раз, когда пользователь меняет пароль,
  даже если это тот же самый пароль, хеш будет уникальным.
- **Адаптивность** — можно увеличивать сложность хеширования со временем, просто изменив параметр количества итераций
  в `bcrypt.gensalt()`. Это полезно с точки зрения безопасности на долгосрочную перспективу.

### 2. **JWT (JSON Web Tokens)**

**JWT** используется для создания токенов, которые удостоверяют личность пользователя после аутентификации. В системе
используются две основные функции: **создание токена** и **декодирование токена**.

- **Функция `encode_jwt`**:
    - Создаёт JWT, используя секретный ключ, алгоритм шифрования и полезную нагрузку (payload).
    - В payload обычно включают такие данные, как идентификатор пользователя (`sub`), дата создания токена (`iat`), и время
      истечения срока действия токена (`exp`).

  Пример:
  ```python
  def encode_jwt(payload: dict[str, tp.Any]) -> str:
      return jwt.encode(
          payload,
          config.auntification.private_key,
          config.auntification.algorithm,
      )
  ```

- **Функция `decode_jwt`**:
    - Декодирует JWT, проверяя его подлинность с помощью публичного ключа и алгоритма шифрования.
    - Эта функция позволяет убедиться, что токен был создан сервером и не был изменён.

  Пример:
  ```python
  def decode_jwt(token: str) -> tp.Any:
      return jwt.decode(
          token,
          config.auntification.public_key,
          algorithms=[config.auntification.algorithm],
      )
  ```

- **Функция `create_jwt`**:
    - Создаёт JWT токен для пользователя на основе его ID и добавляет к payload время истечения действия токена.

  Пример:
  ```python
  def create_jwt(user_id: int) -> str:
      now = datetime.now(timezone.utc)
      return encode_jwt(
          schemas.Payload(
              sub=user_id,
              iat=now,
              exp=now + timedelta(seconds=config.auntification.expires_in),
          ).model_dump()
      )
  ```

**Особенности JWT**:

- **Токен состоит из трёх частей**: заголовок (header), полезная нагрузка (payload) и подпись (signature).
- **Время истечения токена** задаётся параметром `exp`, что позволяет управлять временем жизни токена.
- **Алгоритм шифрования** обычно выбирается из надёжных стандартов, таких как `RS256` или `HS256`.
- **Публичный и приватный ключи** — используются для создания и верификации токенов. Это важно для обеспечения безопасности
  данных, так как приватный ключ должен оставаться только на сервере.

### 3. **API-методы**

#### **Регистрация пользователя (signUp)**

- При регистрации вызывается `hash_password`, чтобы создать хеш пароля перед его сохранением в базе данных.
- После успешной регистрации пользователь добавляется в базу данных.

  Пример:
  ```python
  @router.post("/signUp", response_model=str)
  async def sign_up(
      schema: schemas.Sign,
      session: dependencies.AsyncSession = Depends(dependencies.get_session)
  ):
      user = models.User(
          username=schema.username,
          password=hash_password(schema.password),
      )
      session.add(user)
      await session.commit()
      return "OK"
  ```

#### **Вход в систему (signIn)**

- При попытке входа проверяется наличие пользователя в базе данных.
- Если пользователь найден, проверяется корректность пароля с помощью `check_password`.
- Если пароль верен, создаётся JWT токен с помощью `create_jwt` и возвращается пользователю.

  Пример:
  ```python
  @router.post("/signIn", response_model=schemas.AccessToken)
  async def sign_in(
      schema: schemas.Sign,
      session: dependencies.AsyncSession = Depends(dependencies.get_session)
  ):
      statement = select(models.User).where(models.User.username == schema.username)
      result = await session.exec(statement)
      user = result.one_or_none()

      if user is None or not check_password(schema.password, user.password):
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")

      return schemas.AccessToken(access_token=create_jwt(user.id))
  ```

#### **Смена пароля (changePassword)**

- Проверяется текущий пароль пользователя с помощью `check_password`.
- Если старый пароль верен, новый пароль хешируется с помощью `hash_password`, и изменения сохраняются в базе данных.

  Пример:
  ```python
  @router.post("/changePassword", response_model=str)
  async def change_password(
      schema: schemas.ChangePassword,
      user: tp.Annotated[type[models.User], Depends(dependencies.get_user)],
      session: dependencies.AsyncSession = Depends(dependencies.get_session),
  ):
      if not check_password(schema.old_password, user.password):
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")

      user.password = hash_password(schema.new_password)
      session.add(user)
      await session.commit()

      return "OK"
  ```

### Дополнительные моменты:

1. **Асинхронность** — Важной особенностью является использование асинхронного подхода в работе с базой данных через FastAPI,
   что увеличивает производительность системы при работе с большим числом запросов.
2. **Безопасность** — Пароли не хранятся в открытом виде, а хранятся только их хеши, что снижает риск компрометации. JWT токены
   добавляют уровень защиты через шифрование и проверку подлинности.
3. **Настраиваемое время жизни токена** — Возможность управления временем действия токенов (через параметр `exp`) позволяет
   гибко управлять сессиями пользователей.

Эта система аутентификации может быть легко масштабируема и использует современные подходы для защиты данных и обеспечения
безопасности пользователей.