# Items

-   `Flask` app configured in `app.py`

### Authentication

-   Routes protected with `@jwt_required()`
-   Extra error handlers `expired_token_loader`, `invalid_token_loader`, and `unauthorized_loader` added in `app.py`
-   Claims added to jwt token by `additional_claims_loader` in `app.py`
