Notes:

- Database user should have permissions to create db (**Need for tests**)
- on link '/' you have interface to get access_token and refresh_token. Login
    command overrides previous tokens.
- Added support for refresh_token. If access_token expired you can receive new access_token
- **Callback is registered for domain http://localhost:8000**
