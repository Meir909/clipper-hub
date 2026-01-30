# Google OAuth Setup Instructions

## 1. Создайте Google OAuth приложение

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект или выберите существующий
3. В меню слева выберите "APIs & Services" → "Credentials"
4. Нажмите "Create Credentials" → "OAuth client ID"
5. Выберите "Web application"
6. Добавьте следующие redirect URIs:
   - `http://localhost:5000/auth/login/google/callback`
   - `https://yourdomain.com/auth/login/google/callback` (для production)

## 2. Получите Client ID и Client Secret

После создания приложения вы получите:
- **Client ID** - скопируйте это значение
- **Client Secret** - скопируйте это значение

## 3. Настройте переменные окружения

Создайте файл `.env` в корне проекта:

```env
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
```

Или установите переменные окружения в системе:

### Windows (PowerShell):
```powershell
$env:GOOGLE_CLIENT_ID="your-google-client-id-here"
$env:GOOGLE_CLIENT_SECRET="your-google-client-secret-here"
```

### Windows (CMD):
```cmd
set GOOGLE_CLIENT_ID=your-google-client-id-here
set GOOGLE_CLIENT_SECRET=your-google-client-secret-here
```

## 4. Перезапустите приложение

После настройки переменных окружения перезапустите Flask приложение:

```bash
python run.py
```

## 5. Тестирование

1. Перейдите на страницу входа: http://localhost:5000/auth/login
2. Нажмите "Continue with Google"
3. Вы будете перенаправлены на Google для аутентификации
4. После успешного входа вы вернетесь в приложение

## Как это работает

- При первом входе через Google создается новый пользователь с ролью CLIPPER
- Пользователь получает случайный пароль (не используется для входа через Google)
- Email и имя пользователя автоматически загружаются из Google
- Avatar URL сохраняется для отображения профиля

## Production настройки

Для production:
1. Используйте HTTPS
2. Добавьте домен в authorized redirect URIs в Google Console
3. Настройте правильные переменные окружения на сервере
4. Проверьте настройки безопасности Google OAuth приложения

## Troubleshooting

### Ошибка "redirect_uri_mismatch"
- Убедитесь что redirect URI в Google Console точно совпадает с тем что используется в приложении
- Проверьте что используется правильный протокол (http/https)

### Ошибка "invalid_client"
- Проверьте что Client ID и Client Secret правильные
- Убедитесь что OAuth приложение включено

### Ошибка "access_denied"
- Пользователь отказал в доступе к аккаунту
- Попробуйте еще раз с разрешением доступа
